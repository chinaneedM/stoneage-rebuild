"""Literal pet-name evidence from pinned annual receipts. No new official identity."""
import json
from collections import Counter,defaultdict
from stoneage_pet_history_access import MATRIX,read_pin,ref
from stoneage_pet_source_lookup import ROOT
from stoneage_pet_documentary_access import attach_names,make_rows,materials

SELECTION="research/pets/PET-ANNUAL-NAMED-EVIDENCE-SELECTION-R1.json"
def resolve(x,p):
    for k in p:x=x[k]
    return x
def load_rows():
    m=read_pin(*MATRIX)
    receipts={e["year"]:(e,read_pin(e["receipt"],e["git_blob"])) for e in m["year_receipts"]}
    assert len(receipts)==28
    spec=json.loads((ROOT/SELECTION).read_bytes())
    rows=[]
    for entry in spec["selection"]:
        y=entry["year"]; e,d=receipts[y]; p=entry["pointer"]; raw=resolve(d,p)
        assert entry["region"] in (d.get("region_reviews") or d["region_source_reviews"])
        names=entry["expected_labels"]; assert names and len(names)==len(set(names))
        context=bool(entry.get("context_only",False))
        if entry.get("text"):
            assert isinstance(raw,str) and all(n in raw for n in names)
            pairs=[(n,p) for n in names]
        elif isinstance(raw,list):
            indices=entry.get("select",list(range(len(raw))))
            assert [raw[i] for i in indices]==names
            pairs=[(raw[i],p+[i]) for i in indices]
        else:
            assert isinstance(raw,str) and names==[raw]
            pairs=[(raw,p)]
        for label,lp in pairs:
            # Use source-native paths, not a generated global pet ID.
            source_parent=p[:-1]
            obj=resolve(d,source_parent)
            while not isinstance(obj,dict):
                source_parent=source_parent[:-1];obj=resolve(d,source_parent)
            # A nested claim (e.g. firsthand_reward) has its source metadata
            # higher up; retain the immediate containing object as well.
            anchor=source_parent
            for i in range(len(source_parent),-1,-1):
                parent=resolve(d,source_parent[:i])
                if isinstance(parent,dict) and ("id" in parent or "url" in parent or "source_url" in parent):
                    anchor=source_parent[:i];break
            source_obj=resolve(d,anchor)
            if anchor==[]: source_obj=obj;anchor=source_parent
            extras=entry.get("context_pointers",[])
            for ep in extras:resolve(d,ep)
            rows.append(dict(year=y,region=entry["region"],label=label,role=entry["role"],evidence_grade=entry["grade"],context_only=context,source=ref(e["receipt"],e["git_blob"],lp),source_container=ref(e["receipt"],e["git_blob"],anchor),supplemental_context=[ref(e["receipt"],e["git_blob"],ep) for ep in extras],source_id=source_obj.get("id"),source_date_kind=entry.get("source_date_kind","SOURCE_DATE_AS_WRITTEN_NOT_FIRST_RELEASE"),source_dates={k:v for k,v in source_obj.items() if k in ("date","source_date","period_date","attestation_date","date_display","claimed_event_window","claimed_game_event_year","source_post_date_display","source_edit_date_display","source_event_claim_year","date_kind","source_date_claim")},source_metadata={k:v for k,v in source_obj.items() if k in ("url","urls","source_url","grade","source_grade","source_level","kind","product","product_line")},pet_labels=[] if context else [label],original_field=resolve(d,lp),record=obj,source_record=source_obj,first_release_verified=False,official_same_deployment_identity_verified=False,native_runtime_verified=False,global_unique_species_counted=False))
    counts=attach_names(rows)
    doc_index=defaultdict(list)
    for row in make_rows(materials()):
        for label in row["pet_labels"]:
            doc_index[label].append(dict(directory="documentary",source=row["source"],path=row["source_path"],git_blob=row["git_blob"],pointer=row["pointer"],label=label,qualification="EXACT_LITERAL_LABEL_ONLY_NOT_IDENTITY"))
    for row in rows:
        for name in row["pet_labels"]:
            row["candidate_refs"][name]=row["candidate_refs"][name]+doc_index[name]
    return rows,spec,counts

def filtered(rows,year=None,region=None,q=None,exact=False,context=False):
    return [r for r in rows if (context or not r["context_only"]) and (year is None or year==r["year"]) and (region is None or region==r["region"]) and (not q or (q==r["label"] if exact else q in r["label"]))]

def verify(rows,spec,counts):
    expected=spec["expected"]
    assert len(rows)==expected["records"]==161
    assert len(spec["selection"])==expected["selectors"]==58
    assert len({(r["year"],r["region"],tuple(r["source"]["pointer"]),r["label"],r["role"]) for r in rows})==len(rows)
    pet=[r for r in rows if not r["context_only"]]; ctx=[r for r in rows if r["context_only"]]
    assert len(pet)==expected["petRecords"]==140 and len(ctx)==expected["contextRecords"]==21
    names={r["label"] for r in pet}; assert len(names)==expected["names"]==113
    assert sorted({r["year"] for r in rows})==expected["years"]
    assert all(not r[k] for r in rows for k in ("first_release_verified","official_same_deployment_identity_verified","native_runtime_verified","global_unique_species_counted"))
    assert all(not r["candidate_refs"] for r in ctx)
    assert all(l["qualification"]=="EXACT_LITERAL_LABEL_ONLY_NOT_IDENTITY" and l["label"]==r["label"] for r in pet for l in r["candidate_refs"][r["label"]])
    assert len(filtered(rows,2003,"CN","波比",True))==4
    assert len(filtered(rows,2007,"JP","ギガドラン",True))==2
    assert len(filtered(rows,2008,"KR","도에디크",True))==1
    assert len(filtered(rows,2009,"KR","플라티우스",True))==1
    assert len(filtered(rows,2020,"TW","那提拉",True))==1 and filtered(rows,2020,"TW","那提拉",True)[0]["role"]=="DISPUTED_OPEN_STATUS_PET_LABEL"
    assert len(filtered(rows,2022,"TW","莫可",True))==1
    assert not filtered(rows,2025,"TW","雷爾的意念",True) and len(filtered(rows,2025,"TW","雷爾的意念",True,True))==1
    assert not filtered(rows,2016,"TW","卡恩格登",True) and len(filtered(rows,2016,"TW","卡恩格登",True,True))==1
    assert len(filtered(rows,2023,"TW","里拉拉",True))==1 and len(filtered(rows,2023,"TW","里拉拉",True,True))==2
    assert not filtered(rows,q="메카크로톤",exact=True,context=True) and not filtered(rows,q="사루아치",exact=True,context=True)
    assert not filtered(rows,q="精準(玩家所述技能)",exact=True,context=True)
    assert not filtered(rows,2026) and len(filtered(rows,2026,context=True))==1
    matched={r["label"] for r in pet if r["candidate_refs"][r["label"]]}
    return dict(schema="stoneage.pet.annual_named_access.r1",annual_receipts_checked=28,selected_audit_years=len(expected["years"]),source_label_occurrences=len(rows),pet_label_occurrences=len(pet),context_only_occurrences=len(ctx),distinct_literal_pet_labels=len(names),labels_with_exact_candidate=len(matched),labels_without_exact_candidate=sorted(names-matched),candidate_links_not_identity=sum(len(v) for r in pet for v in r["candidate_refs"].values()),by_region=dict(Counter(r["region"] for r in pet)),by_role=dict(Counter(r["role"] for r in rows)),new_official_release_certifications=0,official_species_count=None,source_bounded_closed=False,**counts)
SUBORDINATE="research/pets/PET-ANNUAL-SUBORDINATE-NAMES-R1.json"
def subordinate_rows(annual):
    spec=json.loads((ROOT/SUBORDINATE).read_bytes())
    pinned={k:read_pin(v["path"],v["git_blob"]) for k,v in spec["pins"].items()}
    assert set(pinned)=={"88","89","114","116","117","119"}
    rows=[]
    for e in spec["selection"]:
        k=str(e["receipt"]); p=spec["pins"][k]; d=pinned[k]
        assert d["year"]==p["year"]
        raw=resolve(d,e["pointer"]); label=e["label"]; src=resolve(d,e["anchor"])
        assert isinstance(raw,str) and (label in raw if e["text"] else label==raw)
        assert p["region"] in ("CN","TW") and "MOBILE" not in e["grade"]
        rows.append(dict(year=p["year"],region=p["region"],receipt="PET"+k,label=label,role=e["role"],evidence_grade=e["grade"],context_only=e["context_only"],source=ref(p["path"],p["git_blob"],e["pointer"]),source_container=ref(p["path"],p["git_blob"],e["anchor"]),pet_labels=[] if e["context_only"] else [label],original_field=raw,record=resolve(d,e["pointer"][:-1]),source_record=src,first_release_verified=False,official_same_deployment_identity_verified=False,native_runtime_verified=False,global_unique_species_counted=False))
    attach_names(rows)
    doc=defaultdict(list)
    for row in make_rows(materials()):
        for name in row["pet_labels"]:
            doc[name].append(dict(directory="documentary",source=row["source"],path=row["source_path"],git_blob=row["git_blob"],pointer=row["pointer"],label=name,qualification="EXACT_LITERAL_LABEL_ONLY_NOT_IDENTITY"))
    for r in rows:
        r["annual_literal_refs"]=[a["source"] for a in annual if a["year"]==r["year"] and a["region"]==r["region"] and a["label"]==r["label"]]
        for label in r["pet_labels"]:r["candidate_refs"][label]+=doc[label]
    pet=[r for r in rows if not r["context_only"]]; ctx=[r for r in rows if r["context_only"]]
    expected=spec["expected"]; names={r["label"] for r in pet}
    assert len(rows)==expected["records"]==59 and len(pet)==expected["petRecords"]==43 and len(ctx)==expected["contextRecords"]==16 and len(names)==expected["distinctPetLabels"]==38
    assert len({(r["receipt"],tuple(r["source"]["pointer"]),r["label"]) for r in rows})==len(rows)
    assert all(not r[k] for r in rows for k in ("first_release_verified","official_same_deployment_identity_verified","native_runtime_verified","global_unique_species_counted"))
    assert not any(r["candidate_refs"] for r in ctx)
    assert all(l["qualification"]=="EXACT_LITERAL_LABEL_ONLY_NOT_IDENTITY" and l["label"]==r["label"] for r in pet for l in r["candidate_refs"][r["label"]])
    assert len(filtered(rows,2012,"CN","塔斯夫",True))==2
    assert not filtered(rows,2012,"CN","坏肯沃",True)
    assert len(filtered(rows,2018,"TW","貝洛寶利",True))==1
    assert not filtered(rows,2020,"TW","米尼樂",True) and len(filtered(rows,2020,"TW","米尼樂",True,True))==1
    assert not filtered(rows,q="血清",exact=True) and len(filtered(rows,q="血清",exact=True,context=True))==1
    assert all(not filtered(rows,q=n,exact=True,context=True) for n in ("푸곤","칼로","메카기로","巧克洛兒"))
    matched={r["label"] for r in pet if r["candidate_refs"][r["label"]]}
    return rows,dict(source_reports=6,source_positions=len(rows),pet_label_positions=len(pet),context_positions=len(ctx),distinct_literal_pet_labels=len(names),labels_with_exact_candidate=len(matched),labels_without_exact_candidate=sorted(names-matched),positions_with_same_year_region_annual_label=sum(bool(r["annual_literal_refs"]) for r in rows),new_official_release_certifications=0,official_species_count=None,limitations=spec["limitations"])

# Explicit retained source positions for the annual names whose literal lookup
# did not hit the other directories. These are not new release attestations.
UNMATCHED_ROOTS={
    "69":("research/recovered/STONEAGE-PET69-YEAR2004-TW75-CNMONKEY-JPAVATAR-R1.json","1907642781be40e6f870c22f6371c1832a35bef2"),
    "70":("research/recovered/STONEAGE-PET70-2004-KR-RIDES-CN75-STAGED-TW-XUANWU-R1.json","8b784a97135aefe3896859e184b0ee71cf9146f4"),
    "72":("research/recovered/STONEAGE-PET72-YEAR2005-CN-TW-JP-KR-SOURCE-R1.json","c71fbd26d908761af8cee1dee42289f6cee06c6c"),
}
ROOT_LABELS={
    "火風鷹人":("69",["region_sources",0,"generic_hawk_label"],"GENERIC_ELEMENT_FAMILY_LABEL_NOT_NATIVE_NAME"),
    **{n:("70",["source_records",0,"named_ride_pets_as_written",i],"RIDING_ROLE_NOT_FIRST_SPECIES_RELEASE") for i,n in enumerate(("라고고","무이","도라비스","고르돈"))},
    **{n:("72",["source_records",0,"names",i],"CN75_PROMOTION_NOT_ACTUAL_GRANT") for i,n in enumerate(("牛头人","鸡年兽"))},
    "ガーヴィ":("72",["source_records",9,"names",0],"CONTEST_PRIZE_PROMISE_NOT_ACTUAL_GRANT"),
    "ヴァンレム":("72",["source_records",10,"names",0],"SHOP_BAG_PLAN_NOT_ACTUAL_GRANT"),
    **{n:("72",["source_records",11,"names",i],"RIDING_ROLE_NOT_FIRST_SPECIES_RELEASE") for i,n in enumerate(("고르고르","타쿠"))},
}
LITERAL_ALTERNATES={
    "火風鷹人":("火风鹰人","SCRIPT_FORM_ONLY"),
    "牛头人":("牛頭人","SCRIPT_FORM_ONLY"),
    "鸡年兽":("雞年獸","SCRIPT_FORM_ONLY"),
    "黑雞":("黑鸡","SCRIPT_FORM_ONLY"),
    "普格多基":("普德多基","CONFLICTING_CHARACTER_NOT_A_SCRIPT_VARIANT"),
    "風地貓卡芙娜":("卡芙娜","DESCRIPTIVE_PREFIX_AND_SHORT_LABEL_SAME_SOURCE"),
    "水火貓卡蘿麗":("卡蘿麗","DESCRIPTIVE_PREFIX_AND_SHORT_LABEL_SAME_SOURCE"),
}
def reconcile_unmatched(annual,sub,report,sub_report):
    expected=set(report["labels_without_exact_candidate"]) | set(sub_report["labels_without_exact_candidate"])
    assert len(expected)==21 and len(ROOT_LABELS)==11
    assert set(ROOT_LABELS)|{"普格多基","黑雞","그램고르","웅이","메가죠","바렌이노","복우리","몽몽","風地貓卡芙娜","水火貓卡蘿麗"}==expected
    docs={k:read_pin(*p) for k,p in UNMATCHED_ROOTS.items()}
    probes=[dict(pet_labels=[alt]) for alt,kind in LITERAL_ALTERNATES.values()]
    attach_names(probes)
    documentary=make_rows(materials())
    alt_refs={}
    for (label,(alt,kind)),p in zip(LITERAL_ALTERNATES.items(),probes):
        refs=list(p["candidate_refs"][alt])
        for r in documentary:
            if alt in r["pet_labels"]:
                refs.append(dict(directory="documentary",source=r["source"],path=r["source_path"],git_blob=r["git_blob"],pointer=r["pointer"],label=alt,qualification="EXACT_LITERAL_LABEL_ONLY_NOT_IDENTITY"))
        assert all(r["label"]==alt for r in refs)
        alt_refs[label]=dict(alternate_label=alt,qualification=kind,directory_candidates=refs,annual_or_subordinate_mentions=[r["source"] for r in annual+sub if r["label"]==alt],same_deployment_identity_verified=False)
    result=[]
    for label in sorted(expected):
        rows=[r for r in annual+sub if r["label"]==label and not r["context_only"]]
        assert rows and all(not r["candidate_refs"][label] for r in rows)
        assert len({(r["year"],r["region"]) for r in rows})==1
        year,region=rows[0]["year"],rows[0]["region"]
        roots=[]
        if label in ROOT_LABELS:
            key,pointer,kind=ROOT_LABELS[label]; d=docs[key]
            assert resolve(d,pointer)==label
            container=pointer[:2]
            source=resolve(d,container)
            assert source["region"]==region and d["year"]==year
            roots.append(dict(source=ref(*UNMATCHED_ROOTS[key],pointer),source_container=ref(*UNMATCHED_ROOTS[key],container),record=source,qualification=kind))
            status="RETAINED_PERIOD_REPORT_NO_NATIVE_ID"
        elif label in ("風地貓卡芙娜","水火貓卡蘿麗"):
            alt,kind=LITERAL_ALTERNATES[label]
            ctx=[r for r in sub if r["receipt"]=="PET119" and r["label"]==alt and r["context_only"]]
            assert len(ctx)==1 and ctx[0]["source_container"]==rows[0]["source_container"]
            roots.append(dict(source=ctx[0]["source"],source_container=ctx[0]["source_container"],qualification="SAME_RECEIPT_SHORT_LABEL_NOT_NEW_PET"))
            status="SAME_RECEIPT_SHORT_LABEL_REFERENCE"
        else:
            status="LATER_RECOLLECTION_OR_HEARSAY_NO_NATIVE_ID"
        # The TW 2005 prize notice is earlier than the 2020 task and contains
        # the short label, but is not proof of identical server pet or grant.
        if label=="風地貓卡芙娜":
            pointer=["source_records",4,"promoted_prizes",1]
            assert resolve(docs["72"],pointer)=="卡芙娜"
            roots.append(dict(source=ref(*UNMATCHED_ROOTS["72"],pointer),source_container=ref(*UNMATCHED_ROOTS["72"],["source_records",4]),record=docs["72"]["source_records"][4],qualification="EARLIER_2005_PRIZE_LABEL_NOT_SAME_DEPLOYMENT_OR_FIRST_RELEASE"))
        if label=="鸡年兽":
            pointer=["source_records",5,"name_candidate"]
            assert resolve(docs["72"],pointer)=="雞年獸"
            roots.append(dict(source=ref(*UNMATCHED_ROOTS["72"],pointer),source_container=ref(*UNMATCHED_ROOTS["72"],["source_records",5]),record=docs["72"]["source_records"][5],qualification="TW_LATER_CHRONOLOGY_NOT_CN75_SAME_ID"))
        item=dict(label=label,year=year,region=region,status=status,original_refs=[r["source"] for r in rows],original_source_containers=[r["source_container"] for r in rows],evidence_grades=sorted({r["evidence_grade"] for r in rows}),retained_source_refs=roots,alternate=alt_refs.get(label),reopen_trigger="QUALIFIED_ORIGINAL_PC_SAME_BUILD_NAME_ID_GRAPHIC_AND_DATED_OPERATOR_OR_ACTUAL_ACQUISITION_EVIDENCE",official_same_deployment_identity_verified=False,first_release_verified=False,global_unique_species_counted=False)
        result.append(item)
    assert sum(x["status"]=="RETAINED_PERIOD_REPORT_NO_NATIVE_ID" for x in result)==11
    assert sum(x["status"]=="SAME_RECEIPT_SHORT_LABEL_REFERENCE" for x in result)==2
    assert all(x["alternate"]["directory_candidates"] for x in result if x["status"]=="SAME_RECEIPT_SHORT_LABEL_REFERENCE")
    assert all(not x["official_same_deployment_identity_verified"] and not x["first_release_verified"] for x in result)
    return result,dict(unmatched_literal_labels=len(result),period_report_root_labels=11,short_label_same_receipt=2,later_recollection_or_hearsay=8,alternate_labels_with_directory_candidates=sorted(x["label"] for x in result if x["alternate"] and x["alternate"]["directory_candidates"]),official_identity_promotions=0,official_species_count=None)

def run(args):
    if args.source or args.version or args.variants: raise SystemExit("annual names support year, region and literal label only")
    if args.exact and not args.query: raise SystemExit("--exact requires --query")
    rows,spec,counts=load_rows(); report=verify(rows,spec,counts)
    sub,sub_report=subordinate_rows(rows); report["subordinate_report_non_additive"]=sub_report
    reconciliation,reconciliation_report=reconcile_unmatched(rows,sub,report,sub_report)
    report["unmatched_literal_reconciliation"]=reconciliation_report
    if args.verify:
        print("PET_ANNUAL_NAMES_PASS "+json.dumps(report,ensure_ascii=False,sort_keys=True));return
    if args.summary or not any((args.year,args.region,args.query)):
        print(json.dumps(dict(**report,limitations=spec["limitations"]),ensure_ascii=False,indent=2));return
    hits=filtered(rows,args.year,args.region,args.query,args.exact,True)
    sub_hits=filtered(sub,args.year,args.region,args.query,args.exact,True)
    if not args.full:
        hits=[{k:v for k,v in r.items() if k not in ("record","source_record","original_field")} for r in hits]
        sub_hits=[{k:v for k,v in r.items() if k not in ("record","source_record","original_field")} for r in sub_hits]
    reconciliation_hits=[r for r in reconciliation if (args.year is None or r["year"]==args.year) and (args.region is None or r["region"]==args.region) and (not args.query or (args.query==r["label"] if args.exact else args.query in r["label"]))]
    if not args.full:
        reconciliation_hits=[dict(r,retained_source_refs=[{k:v for k,v in x.items() if k!="record"} for x in r["retained_source_refs"]]) for r in reconciliation_hits]
    print(json.dumps(dict(unmatched_literal_reconciliation=reconciliation_hits,subordinate_pet_label_evidence=[r for r in sub_hits if not r["context_only"]],subordinate_context_not_pet_release=[r for r in sub_hits if r["context_only"]],filters=dict(year=args.year,region=args.region,query=args.query,exact=args.exact),pet_label_evidence=[r for r in hits if not r["context_only"]],context_not_pet_release=[r for r in hits if r["context_only"]],official_species_count=None,limitations=spec["limitations"]),ensure_ascii=False,indent=2))
