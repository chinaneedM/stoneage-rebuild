"""PET55 custody: independently verify both actual derived artifacts, preserve raw JSON."""
import hashlib, json, zipfile, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"research/pets"
RUNS=[
(45472910262,138725365545,14958008781,13566,"31a9d88b62f728278074c50160c5ea596be43832358fd0633b0d4e678b0b2214"),
(45472921828,138725407235,14958756074,13565,"2f64c008801cc7c58f2d1a87a5d249b68f9eca7389f899c522de1f83272f4c0b")]
CANDIDATE="c450c95d2060b292c583819389a7abc3cc4d88d0"
def sha(b): return hashlib.sha256(b).hexdigest()
def blob(b): return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def verify():
    expected=json.loads((P/"PET-HIGH-FIRST-55-LATER-FUSION-HATCHING-R1.json").read_bytes())
    prior=json.loads((P/"PET-HIGH-FIRST-54-EGG-FUNCTION-STATIC-PROBE-R1.json").read_bytes())
    prior_accepted=json.loads((P/"PET-HIGH-FIRST-54-EGG-ROLE-AND-FUNCTION-ACCEPTED-R1.json").read_bytes())
    reports=[]; receipts=[]
    for run,job,artifact,n,digest in RUNS:
        raw=Path("/tmp/pet55-"+str(artifact)+".zip").read_bytes()
        assert len(raw)==n and sha(raw)==digest
        with zipfile.ZipFile(Path("/tmp/pet55-"+str(artifact)+".zip")) as z:
            assert z.namelist()==["pet55-derived.json"]
            content=z.read("pet55-derived.json")
        d=json.loads(content); reports.append(d)
        assert d["schema"]=="stoneage.pet55.source_replay.r1"
        assert {p:v["git_blob"] for p,v in d["comparison_receipts"].items()}==expected["comparison"]["git_blobs"]
        assert len(d["comparison_receipts"])==18
        o=d["original"]
        assert o["executable_sha256"]==expected["original"]["exe_sha256"]
        assert not o["field_offsets_verified"] and not o["runtime_executed"] and not o["indirect_control_flow_complete"]
        assert len(o["symbols"])==10
        assert [x["target"] for x in o["symbols"] if x["exact_symbols"]]==["NPC_EventAddEgg"]
        assert all(x["status"]=="NOT_FOUND_IN_TEXT_SYMBOL_TABLE" and not x["intervals"] for x in o["symbols"] if x["target"]!="NPC_EventAddEgg")
        f=o["symbols"][0]["intervals"][0]
        assert f["start"]==4896128 and f["end"]==4897696 and f["instruction_count"]==409
        assert f["body_sha256"]==prior["probe"]["body_disassembly_sha256"]
        assert f["body_sha256"]==prior_accepted["original_executable"]["body_sha256"]
        assert d["official_acquisition_closed"]==0 and not d["actual_hatching_verified"] and not d["original_assets_published"]
        name="PET-HIGH-FIRST-55-SOURCE-REPLAY-"+str(run)+"-R1.json"
        (P/name).write_bytes(content)
        receipts.append({"run":run,"job":job,"artifact":artifact,"zip_bytes":n,"zip_sha256":digest,"report":name,"report_bytes":len(content),"report_sha256":sha(content),"report_git_blob":blob(content)})
    assert reports[0]["comparison_receipts"]==reports[1]["comparison_receipts"]
    assert reports[0]["original"]["symbols"]==reports[1]["original"]["symbols"]
    result={"schema":"stoneage.pet55.custody.r1","candidate":CANDIDATE,"receipts":receipts,"comparison_receipts_equal":True,"original_symbol_probes_equal":True,"raw_reports_equal":receipts[0]["report_sha256"]==receipts[1]["report_sha256"],"original_exact_symbol_found_count":1,"original_exact_symbol_absent_count":9,"original_deployment_bridge":False,"strict_gap_count":67,"official_acquisition_closed":0,"original_payload_published":False}
    (P/"PET-HIGH-FIRST-55-SOURCE-CUSTODY-R1.json").write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    print("PET55_CUSTODY",json.dumps(result,sort_keys=True))
if __name__=="__main__": verify()
