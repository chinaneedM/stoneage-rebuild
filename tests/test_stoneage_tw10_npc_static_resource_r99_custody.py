"""R99 independent immutable source-custody receipt guards."""
import copy
import json
import unittest
from pathlib import Path
from tools.stoneage_pet_asset_growth_catalog import ROOT,gitblob
from tools.stoneage_tw10_npc_static_resource_r99 import audit,check_saved
P=ROOT/"research/recovered/STONEAGE-TW10-NPC-STATIC-RESOURCE-JOIN-ACCEPTANCE-R99.json"
EXPECTED_RECEIPT="0a1e7fb7ff82efe44e017fabb4ef11c712e27a0a"
SOURCE=ROOT/"research/recovered/STONEAGE-TW10-NPC-STATIC-RESOURCE-JOIN-R99.json"
SOURCE_SHA="21d49800a1191f87a006aaa5af4a6f7975f91bf7"

def verify(d):
    raw=P.read_bytes()
    assert gitblob(raw)==EXPECTED_RECEIPT,"R99 custody receipt changed"
    assert d==json.loads(raw.decode("utf-8")),"R99 receipt mutation"
    assert gitblob(SOURCE.read_bytes())==SOURCE_SHA,"R99 original derived metadata changed"
    assert check_saved(audit()),"R99 live source replay differs from archival report"
    assert d["schema"]=="stoneage.tw10_original_static_resource_join_r99_acceptance.v1"
    assert d["initial_main"]["sha"]=="1ab3968decb3ee9abde1898d4e63a18ff176ad2e"
    assert d["commits"]["docs_main"]["sha"]=="a4628bec7b2aac33feb33980a9ef7660494bea24"
    assert (len(d["candidate_all_runs"]),len(set(d["candidate_all_runs"])))==(10,10)
    assert (len(d["main_all_runs"]),len(set(d["main_all_runs"])))==(11,11)
    assert set(d["candidate_all_runs"]).isdisjoint(d["main_all_runs"])
    assert [x["methods"] for x in d["source_runs"]]==[13,14,15,15]
    assert [x["run"] for x in d["source_runs"]]==[39970753998,39971115264,39972087601,39972245520]
    assert [x["job"] for x in d["source_runs"]]==[120472469976,120473726586,120477120997,120477669326]
    assert [x["artifact_id"] for x in d["source_runs"]]==[12508399205,12509006934,12509711942,12509283397]
    assert len({x["artifact_id"] for x in d["source_runs"]})==4
    assert all(x["success"] and x["artifact_zip_bytes"]==7625 and len(x["artifact_zip_sha256"])==64 for x in d["source_runs"])
    assert d["derived_source"]["git_blob"]==SOURCE_SHA
    assert d["derived_source"]["raw_sha256"]=="9b73469fef2ebe27a4369ecc76e8cb57d0ef853ffb4f87d2228609c7a8b52ee1"
    assert len(d["preserved_historical_prefixes"])==4
    assert all(x["prefix_exact"] and len(x["old_blob"])==len(x["new_blob"])==40 for x in d["preserved_historical_prefixes"])
    p=d["main_publication"]
    assert p["compare_ahead"]==3 and p["compare_behind"]==0 and p["changed_files"]==9 and p["deletions"]==0
    assert p["nonforce_expected_sha_fast_forward"] and p["candidate_ci_all_success"] and p["main_ci_all_success"]
    assert d["verified_physical_findings"]["rows"]==101 and d["verified_physical_findings"]["distinct_rd_block_hashes"]==101
    assert d["verified_physical_findings"]["first_run"]=={"bitmap":[5846,5919],"map_resource":[16000,16073],"rows":74}
    assert d["verified_physical_findings"]["second_run"]=={"bitmap":[5920,5946],"map_resource":[16200,16226],"rows":27}
    assert d["verified_physical_findings"]["original_spr_frame_records_examined"]==242085
    assert d["verified_physical_findings"]["zero_direct_spr_references"] is True
    assert all(d["boundaries"][k] is False for k in ("original_NPC_identity_proven","world_floor_map_number_proven","original_server_NPC_spawn_verified","original_game_render_execution_verified","native_image_pixels_archived","original_art_reuse_approved","stage_a_closed","stage_b_started"))
    assert d["boundaries"]["overall_restoration_percent"] is None
    assert d["boundaries"]["next"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-100"
    return True

class R99Custody(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.d=json.loads(P.read_text(encoding="utf-8"))
    def reject(self,f):
        d=copy.deepcopy(self.d);f(d)
        with self.assertRaises(AssertionError):verify(d)
    def test_original_receipt(self):self.assertTrue(verify(self.d))
    def test_changed_stage(self):self.reject(lambda d:d["boundaries"].update(stage_a_closed=True))
    def test_false_npc_identity(self):self.reject(lambda d:d["boundaries"].update(original_NPC_identity_proven=True))
    def test_extra_fake_ci(self):self.reject(lambda d:d["candidate_all_runs"].append(1))
    def test_artifact_mutation(self):self.reject(lambda d:d["source_runs"][3].update(artifact_id=12508399205))
    def test_unproven_original_pixels(self):self.reject(lambda d:d["boundaries"].update(native_image_pixels_archived=True))
    def test_rebuilt_report_conflict(self):self.reject(lambda d:d["verified_physical_findings"]["second_run"].update(rows=28))
if __name__=="__main__":unittest.main()
