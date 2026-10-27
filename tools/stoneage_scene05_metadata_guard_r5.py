"""Verify source-qualified R5 SAFE receipts. Does not load proprietary images."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"research/recovered/STONEAGE-SCENE05-REAL-PIXEL-PUBLICATION-R5.json"

def qualify(r):
    assert r["schema"]=="stoneage.scene05.real_source_pixel_publication.r5"
    assert r["source_role"]=="PRESERVED_COMMUNITY_MIXED25_NOT_OFFICIAL_TW1"
    s=r["source"]
    assert (s["action_run"],s["action_conclusion"],s["artifact_id"])==(40604115589,"success",12779831795)
    assert s["source_original_real_sha256"]=="c7640643804d550bc07e33661103fb7b5f557ee01e68a5a5d92382c5305c2b0d"
    assert s["artifact_safe_json_sha256"]=="38d870513edebf93edb0d7df6119f4473353b3d2b0bc3a64641bbc57915e42c8"
    assert [v["map_id"] for v in r["rows"]]==[5009,5015]
    for item,i,offset,length,sha in zip(r["rows"],[1624,1630],[2381236,2389112],[1698,1656],[
        "3ade98b2ff9d081eb8b315a220623be22bfd47206e3e34f609fd3ecd638c9e95",
        "4c65fd86cb1b783914c7e2d3a26623a619d0945f0ac0baa08bd16fede599daa2"]):
        assert (item["adrn_record_index"],item["real_offset"],item["RD_length"])==(i,offset,length)
        assert item["RD_flag"]==1 and item["RD_sha256"]==sha
        assert item["dimension"]==[64,47] and item["source_reserved_palette_slots"]==[]
    x=r["replay"]
    assert all(x[k] is True for k in ["source_original_8_images_independent_RD_pixel_exact","new_two_independent_RD_pixel_exact","all_10_images_source_palette_candidate","private_library_upload_and_full_independent_readback","browser_pan_zoom_layers_reset"])
    assert x["actual_source_image_count"]==x["browser_images_loaded"]==10
    assert x["actual_DAT_reference_count"]==x["browser_refs_seen"]==30
    assert x["missing_image_ids"]==[] and x["browser_javascript_errors"]==0
    assert x["private_observer_html_sha256"]=="ff9c99fa3df6ccbc162ea87e87f5cd8e4a980e3b0f9877309f99d30776dae298"
    assert x["private_bundle_sha256"]=="88cb122f3f14aadb1bf70bfcdccfe5911a43813d5f47aef0dd341cada25b9c88"
    assert x["original_deployed_palette_or_occlusion_proven"] is False
    q=r["limits"]
    assert q["commercial_original_client_executed"] is False and q["original_playable_world_entered"] is False
    assert q["historical_same_build_qualified"] is False
    assert q["original_palette_runtime_qualified"] is False and q["original_full_occlusion_qualified"] is False
    assert q["stage_A"]=="7_PARTIAL_2_OPEN" and q["stage_B"]==q["wiki"]=="GATED"
    assert q["overall_percent"] is None
    return True

class ReceiptGuard(unittest.TestCase):
    def setUp(self):
        self.r=json.loads(PATH.read_text())
    def test_current_receipt(self):
        self.assertTrue(qualify(self.r))
    def test_mutation_fake_world_entry_rejected(self):
        a=copy.deepcopy(self.r);a["limits"]["original_playable_world_entered"]=True
        with self.assertRaises(AssertionError):qualify(a)
    def test_mutation_original_palette_claim_rejected(self):
        a=copy.deepcopy(self.r);a["replay"]["original_deployed_palette_or_occlusion_proven"]=True
        with self.assertRaises(AssertionError):qualify(a)
    def test_mutation_pixel_absent_rejected(self):
        a=copy.deepcopy(self.r);a["replay"]["new_two_independent_RD_pixel_exact"]=False
        with self.assertRaises(AssertionError):qualify(a)
    def test_mutation_missing_source_restored_rejected(self):
        a=copy.deepcopy(self.r);a["replay"]["missing_image_ids"]=[5015]
        with self.assertRaises(AssertionError):qualify(a)
    def test_mutation_source_sha_rejected(self):
        a=copy.deepcopy(self.r);a["rows"][0]["RD_sha256"]="f"*64
        with self.assertRaises(AssertionError):qualify(a)
    def test_mutation_right_count_rejected(self):
        a=copy.deepcopy(self.r);a["replay"]["actual_DAT_reference_count"]=29
        with self.assertRaises(AssertionError):qualify(a)

if __name__=="__main__":unittest.main()
