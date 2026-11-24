"""PET57: retain two identical generated coverage artifacts and extend existing source manifest."""
import hashlib,json,zipfile
from pathlib import Path
from tools.stoneage_pet_high_first_57_coverage import ROOT,P,TARGET,build,blob
RUNS=[(45477710013,138742229420,14959872699),(45477719354,138742262022,14961031196)]
ZIP_SHA="5f7bbe13a5d64531af785f01cada05e26c01351f10bd3b19be4494b6eaa0b6f9"
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    reports=[];receipts=[]
    for run,job,art in RUNS:
        p=Path("/tmp/pet57-"+str(art)+".zip");raw=p.read_bytes()
        assert len(raw)==32113 and sha(raw)==ZIP_SHA
        with zipfile.ZipFile(p) as z:
            assert z.namelist()==[TARGET.name]
            c=z.read(TARGET.name)
        reports.append(c);receipts.append({"run":run,"job":job,"artifact":art,"zip_bytes":len(raw),"zip_sha256":sha(raw),"report_bytes":len(c),"report_sha256":sha(c),"report_git_blob":blob(c)})
    assert reports[0]==reports[1]
    TARGET.write_bytes(reports[0])
    d=json.loads(reports[0]);s=d["summary"]
    assert (s["template_positions"],s["distinct_graphics"],s["tw85_physical_graphic_positions"],s["tw85_unique_physical_groups"],s["positions_with_any_same_number_tw85_frame_mapping"])==(67,66,67,66,67)
    assert (s["distinct_named_grid_portrait_aliases"],s["aliases_with_exact_native_candidates"],s["positions_with_name_only_portrait_candidates"])==(56,56,57)
    assert not s["positions_without_tw85_physical_graphic"] and s["positions_without_exact_name_grid"]==[108,109,110,111,309,317,318,330,386,454]
    assert s["strict_gap_count"]==67 and s["official_acquisition_closed"]==0
    assert all(r["retain_strict_gap"] and not r["official_acquisition_verified"] for r in d["rows"])
    assert (json.dumps(build(),ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode()==reports[0]
    result={"schema":"stoneage.pet57.coverage_custody.r1","candidate":"a40baab08d0e2770bf560dde952e71aa894606f8","receipts":receipts,"dual_zip_identical":True,"dual_report_identical":True,"independent_replay_identical":True,"summary":s,"original_payload_published":False}
    custody=P/"PET-HIGH-FIRST-57-COVERAGE-CUSTODY-R1.json"
    custody.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    manifest=P/"PET-HIGH-FIRST-32-UNIFIED-SOURCE-LOOKUP-MANIFEST-R1.json"
    m=json.loads(manifest.read_bytes())
    assert "hf57" not in m["sources"]
    m["sources"]["hf57"]={"path":str(TARGET.relative_to(ROOT)),"git_blob":blob(reports[0]),"expected_array":"rows","expected_rows":67}
    m["supplement_hf57"]={"source_head":"a40baab08d0e2770bf560dde952e71aa894606f8","source_tree":"f765cdc22c2ef3d5252b5c9e7801457fe5431502","scope":"67 existing residual template positions; complete same-number TW85 physical group and frame mapping coverage, 57 exact written-name album candidates, 56 alias candidates; no official identity or acquisition closure."}
    manifest.write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n")
    lookup=ROOT/"tools/stoneage_pet_source_lookup.py"
    raw=lookup.read_bytes()
    assert blob(raw)=="8fb82ae1410f07464eee8e9ffd6be233b96a49da"
    text=raw.decode("utf-8")
    for before,after in [["    special56_by_position = by_id(d[\"hf56\"][\"rows\"], \"position\")","    coverage57_by_position = by_id(d[\"hf57\"][\"rows\"], \"position\")\n    special56_by_position = by_id(d[\"hf56\"][\"rows\"], \"position\")"],["        if i in special56_by_position:","        if i in coverage57_by_position:\n            j57 = coverage57_by_position[i]\n            r57 = d[\"hf57\"][\"rows\"][j57]\n            assert (r57[\"template_id\"], r57[\"graphic\"], r57[\"master_row_sha256\"]) == (k, x[\"graphic\"], x[\"row_sha256\"])\n            ls.append(link(\"hf57\", [\"rows\", j57], \"SAME_NUMBER_PHYSICAL_ASSET_AND_INDEPENDENT_NAME_EVIDENCE_NOT_OFFICIAL_IDENTITY\"))\n        if i in special56_by_position:"],["    assert source_counts[\"hf56\"] == 10 and source_counts[\"hf56_replay\"] == 14 and source_counts[\"hf56_preflight\"] == 5","    assert source_counts[\"hf57\"] == 67\n    assert {i for i,e in enumerate(high45) if any(l[\"source\"]==\"hf57\" for l in e[\"linked_records\"])} == set(d[\"hf49\"][\"remaining_gap_row_indices\"])\n    assert all(r[\"retain_strict_gap\"] and not r[\"official_acquisition_verified\"] for r in d[\"hf57\"][\"rows\"])\n    assert source_counts[\"hf56\"] == 10 and source_counts[\"hf56_replay\"] == 14 and source_counts[\"hf56_preflight\"] == 5"]]:
        assert text.count(before)==1
        text=text.replace(before,after)
    lookup.write_bytes(text.encode("utf-8"))
    print("PET57_CUSTODY",json.dumps(result,ensure_ascii=False,sort_keys=True))
if __name__=="__main__":main()
