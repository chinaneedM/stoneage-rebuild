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
def run(args):
    if args.source or args.version or args.variants: raise SystemExit("annual names support year, region and literal label only")
    if args.exact and not args.query: raise SystemExit("--exact requires --query")
    rows,spec,counts=load_rows(); report=verify(rows,spec,counts)
    if args.verify:
        print("PET_ANNUAL_NAMES_PASS "+json.dumps(report,ensure_ascii=False,sort_keys=True));return
    if args.summary or not any((args.year,args.region,args.query)):
        print(json.dumps(dict(**report,limitations=spec["limitations"]),ensure_ascii=False,indent=2));return
    hits=filtered(rows,args.year,args.region,args.query,args.exact,True)
    if not args.full:
        hits=[{k:v for k,v in r.items() if k not in ("record","source_record","original_field")} for r in hits]
    print(json.dumps(dict(filters=dict(year=args.year,region=args.region,query=args.query,exact=args.exact),pet_label_evidence=[r for r in hits if not r["context_only"]],context_not_pet_release=[r for r in hits if r["context_only"]],official_species_count=None,limitations=spec["limitations"]),ensure_ascii=False,indent=2))
