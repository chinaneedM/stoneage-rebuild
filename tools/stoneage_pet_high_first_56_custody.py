"""PET56 exact dual artifact custody plus original NPC hit reconciliation."""
import hashlib,json,zipfile
from collections import Counter
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"research/pets"
R=P.parent/"recovered"
RUNS=[
(45475208972,138733483969,14958099882,11530,"019364a0dd44c85aea290c444ff5cf30cbf9cc85ec12049b7093e829199a6274"),
(45475216473,138733512823,14958593729,11528,"ff89b1cefe5374a37930009b78c4c0fd999c1edb43ab3a1555be69ce6676986d")]
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def load(path,pin=None):
    raw=path.read_bytes()
    if pin:assert blob(raw)==pin
    return json.loads(raw)
def validate(d,pre,old,manifest):
    assert d["schema"]=="stoneage.pet56.original_all_residual_typed_reference_probe.r1"
    assert {p:v["git_blob"] for p,v in d["comparison_receipts"].items()}==pre["later_source"]["pins"]
    rows=old["projection"]["records"]
    assert len(rows)==67
    ids={i["instance_id"]:r for r in rows for i in r["source_pairs"][0]["instances"]}
    assert len(ids)==70 and sorted(ids)==d["target_selected_instance_ids"]
    assert sorted(r["template_id"] for r in rows)==d["target_template_ids"]
    o=d["original_receipt"]
    assert (o["unique_member_count"],o["member_bytes"],o["headers_visited"],o["range_bytes"],len(o["range_receipts"]))==(2207,2300545,7954,12013836,184)
    assert len(d["original_later_paths_absent"])==4
    f={x[0]:x for x in manifest["source_files"]}
    refs=Counter(x[0] for row in manifest["create_rows"] for x in row[-1])
    assert len(f)==2205 and len(manifest["create_rows"])==4985
    assert all(p.removeprefix("npc/") not in f for p in d["original_later_paths_absent"])
    s=d["scan"];hits=s["typed_candidate_lines"]
    assert s["lexical_collision_lines"]==1438 and s["typed_candidate_count"]==len(hits)==14
    assert Counter(x["fields"][0]["field"] for x in hits)=={"vippet":2,"addpet":12}
    trainer=next(x for x in old["projection"]["npc_source_files"] if x["path"]=="sa60/newbie/m_tiger")
    t={x["line"]:x for x in trainer["candidate_lines"] if x["key"]=="AddPet"}
    assert len(t)==12 and refs["sa60/newbie/m_tiger"]==4
    assert sorted(x["floor"] for x in trainer["create_refs"])==[1040,2030,3030,4030]
    v=[]
    for h in hits:
        p=h["path"].removeprefix("npc/")
        assert h["file_sha256"]==f[p][2] and len(h["fields"])==1
        field=h["fields"][0]; ident=field["instance_ids"][0]
        if field["field"]=="addpet":
            assert p=="sa60/newbie/m_tiger"
            prev=t[h["line"]]
            assert h["line_sha256"]==prev["source_line_sha256"] and field["instance_ids"]==prev["matching_instance_tokens"]
            assert ids[ident]["template_id"] in (161,162,163,164)
        else:
            assert p in ("my/vipshop/暂不用.arg","my/vipshop/暂不用.arg.bak") and refs[p]==0
            assert ident==323 and ids[ident]["template_id"]==231 and h["line"]==181
            v.append(h)
    assert len(v)==2 and v[0]["file_sha256"]!=v[1]["file_sha256"] and v[0]["line_sha256"]==v[1]["line_sha256"]
    assert not d["original_payload_published"] and not d["runtime_executed"] and d["official_acquisition_closed"]==0
    return ids,refs
def main():
    pre=load(P/"PET-HIGH-FIRST-56-SPECIAL-ROLE-PREFLIGHT-R1.json")
    old=load(P/"PET-HIGH-FIRST-50-ORIGINAL-ACQUISITION-R1.json","4d0b31a7fa196cf8f227a7b0b1aea7183d9598f0")
    manifest=load(R/"STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json","a088b61a3212f7049e7793f587123ffb29bebad7")
    reports=[]; receipts=[]
    for run,job,art,n,h in RUNS:
        path=Path("/tmp/pet56-"+str(art)+".zip")
        raw=path.read_bytes()
        assert len(raw)==n and sha(raw)==h
        with zipfile.ZipFile(path) as z:
            assert z.namelist()==["pet56-derived.json"]
            content=z.read("pet56-derived.json")
        d=json.loads(content)
        ids,refs=validate(d,pre,old,manifest)
        reports.append(d)
        name="PET-HIGH-FIRST-56-SOURCE-REPLAY-"+str(run)+"-R1.json"
        (P/name).write_bytes(content)
        receipts.append({"run":run,"job":job,"artifact":art,"zip_bytes":n,"zip_sha256":h,"report":name,"report_bytes":len(content),"report_sha256":sha(content),"report_git_blob":blob(content)})
    a,b=reports
    assert a["comparison_receipts"]==b["comparison_receipts"] and a["scan"]==b["scan"]
    assert a["original_receipt"]["member_ledger_sha256"]==b["original_receipt"]["member_ledger_sha256"]
    groups=[]
    for i,row in enumerate(pre["rows"]):
        groups.append(dict(row,preflight_index=i,source_hit_indices=[],qualification=row["role"],retain_strict_gap=True))
    for ident in (2481,2482,2483,2484,323):
        r=ids[ident]
        groups.append({"position":r["tw75_row_index"],"name":r["name"],"template":r["template_id"],"instance":ident,"graphic":r["graphic"],"qualification":"SAVED_TRAINER_REWARD_ALREADY_RECORDED_NOT_OFFICIAL_AWARD" if ident!=323 else "UNREFERENCED_RESERVED_VIP_NUMERIC_CANDIDATE_NOT_OFFICIAL_AWARD","source_hit_indices":[i for i,h in enumerate(a["scan"]["typed_candidate_lines"]) if ident in h["fields"][0]["instance_ids"]],"retain_strict_gap":True,"official_acquisition_verified":False})
    result={"schema":"stoneage.pet56.special_role_custody.r1","candidate":"b8be40dd47ce44902afc2cada75c83b3490cdecb","receipts":receipts,"comparison_receipts_equal":True,"scan_equal":True,"original_member_ledger_equal":True,"raw_reports_equal":receipts[0]["report_sha256"]==receipts[1]["report_sha256"],"rows":groups,"strict_gap_count":67,"official_acquisition_closed":0,"official_species_count":None,"original_payload_published":False}
    (P/"PET-HIGH-FIRST-56-SOURCE-CUSTODY-R1.json").write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    print("PET56_CUSTODY",json.dumps(result,ensure_ascii=False,sort_keys=True))
if __name__=="__main__":main()
