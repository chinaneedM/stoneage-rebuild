"""Acceptance smoke test of the existing source-separated PET delivery entry points."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CLI=ROOT/"tools/stoneage_pet_source_lookup.py"
P=ROOT/"research/pets"
def pin(name,expected):
    b=(P/name).read_bytes()
    assert hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==expected,name
    return json.loads(b)
def cli(*args,parse=True):
    p=subprocess.run([sys.executable,str(CLI),*args],cwd=ROOT,check=True,capture_output=True,text=True,encoding="utf-8",timeout=90)
    return json.loads(p.stdout) if parse else p.stdout
def main():
    old=pin("PET-FINAL-REVIEW-MATRIX-R1.json","8a3694119db2c0b83dbe6b0c54fc7d912a8493c6")
    receipt=pin("PET-FINAL-REVIEW-ACCEPTANCE-RECEIPT-R1.json","e8586bb4c6db5550cc6ece3c73dec3312ea5959b")
    assert receipt["artifact"]["independently_downloaded_and_crc_checked"] and receipt["artifact"]["full_json_committed"]
    assert receipt["artifact"]["json_sha256"]==hashlib.sha256((P/"PET-FINAL-REVIEW-MATRIX-R1.json").read_bytes()).hexdigest()
    updater=pin("PET-CN2013-UPDATER-PATH-WITNESSES-R1.json","58f204e9df34f29457cc12b1552e8de382357514")
    assert updater["original_client_verified"] is False and updater["pet_payload_extracted"] is False
    modes=[(),("--legacy-pet16",),("--documentary",),("--history",),("--annual-names",),("--kr-archive",)]
    for mode in modes:
        cli(*mode,"--verify",parse=False)
    current,legacy,doc,hist,annual,kr=[cli(*mode,"--summary") for mode in modes]
    assert current["source_record_occurrences"]==5924 and current["literal_labels"]==1046
    assert legacy["total_source_rows"]==2792 and legacy["unknown_cn_web_names"]==6
    assert doc["documentary_records"]==140 and doc["official_release_events_previously_documented"]==9
    assert hist["annual_receipts_verified"]==28 and hist["region_year_receipts"]==156 and hist["open_years"]==[2026]
    assert annual["source_label_occurrences"]==161 and annual["pet_label_occurrences"]==140
    assert annual["subordinate_report_non_additive"]["source_positions"]==59
    assert annual["unmatched_literal_reconciliation"]["unmatched_literal_labels"]==21
    assert kr["source_blobs"]["research/pets/PET-KR2003-GIF-RETRY-CI-OBSERVED-R1.json"]=="dbef9c310a5821df0f240cb054baa411058e8447"
    k=kr["summary"]
    assert (k["distinct_reference_paths"],k["exact_decoded_gifs"],k["unmatched_reference_paths"],k["decoded_frames"])==(159,32,127,54)
    assert all(x["official_species_count"] is None for x in (current,legacy,doc,hist,annual,k,old))
    assert old["queue_positions"]==3563 and old["manifest_sources"]==98 and old["carrier_groups_reviewed"]==15
    assert old["official_full_fields_certified"]==0 and not old["source_bounded_closed"] and not old["historically_complete"]
    # Actual CLI full queries across all access lanes, never merge or add counts.
    q=cli("--source","tw10","--query","PET-000001","--exact","--full")
    assert q["source_occurrences"]==1 and "original_source_record" in q["results"][0]
    q=cli("--legacy-pet16","--source","cn_official_web","--query","web_ordinal:1","--exact","--full")
    assert q["source_occurrences"]==1 and q["results"][0]["name"] is None
    q=cli("--documentary","--source","cn2004_trainers","--query","猛毒攻击","--exact","--full")
    assert sorted(r["record"]["listed_price"] for r in q["results"] if r["kind"]=="trainer_skill_claim")==[4000,4400]
    q=cli("--history","--year","2026","--region","TW","--full")
    assert len(q["years"])==1 and q["years"][0]["year_review_status"]=="NOT_YEAR_AUDITED"
    q=cli("--annual-names","--year","2020","--query","風地貓卡芙娜","--exact","--full")
    assert q["unmatched_literal_reconciliation"]
    q=cli("--kr-archive","--query","4_024.gif","--exact","--full")
    assert q["count"]==1 and q["results"][0]["status"]=="EXACT_ARCHIVE_GIF_DECODED" and q["results"][0]["pet_name"] is None
    q=cli("--kr-archive","--query","4_001.gif","--exact","--full")
    assert q["count"]==1 and q["results"][0]["status"]=="NO_MATCH_IN_BOUNDED_CDX" and "gif" not in q["results"][0]
    assert cli("--query","NOT_A_HISTORICAL_PET_000","--exact")["source_occurrences"]==0
    report={"schema":"stoneage.pet.module_delivery_review.r1","verified_query_modes":6,"full_query_probes":8,"current":current,"legacy":legacy,"documentary":doc,"chronology":hist,"annual_names":annual,"korean_archive":kr,"matrix":{"git_blob":"8a3694119db2c0b83dbe6b0c54fc7d912a8493c6","pinned_sources":98,"carrier_groups":15,"field_queue_positions":3563,"seven_dimensions":old["seven_dimensions"],"official_full_fields_certified":0},"post_matrix_carrier_notes":{"KR2002_2003":"Exact original responses and GIF bytes transiently verified, separate source paths; original images not retained privately","CN2013_UPDATER":"Path tokens only, not original pet payload; no identity promotion"},"scope":"Fixed accessible source delivery and actual lookup smoke test, not exhaustive discovery or historical completion. Independent source counts overlap and are not additive.","official_species_count":None,"historically_complete":False,"source_bounded_closed":False,"user_authorized_switch_to_npc":False,"active_module":"PET","original_assets_published":False,"remaining":["User review of bounded delivery and explicit module transition authorization.","Reopen only material source or field gaps using the matrix conditions; 2026 remains open."]}
    print("PET_MODULE_DELIVERY_REVIEW_PASS 6 access modes, 8 full/negative query probes; historical completion false")
    (ROOT/"pet-module-delivery-review.json").write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
