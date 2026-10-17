"""Raw source artifact, Git blob and semantic recomputation replay for item bitmap bridge."""
import hashlib
import json
import unittest
from pathlib import Path
from tools.stoneage_tw10_item_static_bitmap_source import observe

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-TW10-ITEM-STATIC-BITMAP-SOURCE-R1.json"
ACCEPTANCE=ROOT/"research/recovered/STONEAGE-TW10-ITEM-STATIC-BITMAP-SOURCE-ACCEPTANCE-R1.json"
EXPECTED_RAW_SHA="9916bab4e8b94188e8b4dc9c0e5f6cd2537464311f3c3409a6a04d72fffec2b8"
EXPECTED_BLOB_SHA="1210b0f910c353d58a3d6a4c458dda38f48aba86"

class StaticItemArchiveReplay(unittest.TestCase):
    def test_fixed_original_artifact_bytes(self):
        content=REPORT.read_bytes()
        self.assertEqual(len(content),21307)
        self.assertEqual(hashlib.sha256(content).hexdigest(),EXPECTED_RAW_SHA)
        self.assertEqual(hashlib.sha1(b"blob "+str(len(content)).encode()+b"\0"+content).hexdigest(),
                         EXPECTED_BLOB_SHA)
        r=json.loads(ACCEPTANCE.read_text(encoding="utf-8"))["permanent_source"]
        self.assertEqual(r["downloaded_original_zip_sha256"],
                         "04900b9b905610a5ae0c7b148ef8c9a12898059683fb0c35efc92fadd0b3f2c9")
        self.assertEqual(r["downloaded_raw_member_sha256"],EXPECTED_RAW_SHA)
        self.assertEqual(r["archived_git_blob_sha"],EXPECTED_BLOB_SHA)
        self.assertTrue(r["independent_zip_and_raw_checks"])

    def test_semantic_replay_exact_and_no_gameplay_promotion(self):
        expected=(json.dumps(observe(),ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")
        self.assertEqual(REPORT.read_bytes(),expected)
        d=json.loads(REPORT.read_text(encoding="utf-8"))
        item=next(x for x in d["bitmap_metadata_bands"] if x["player_category_id"]=="items")
        self.assertEqual(item["original_bitmap_id_membership_count"],1031)
        self.assertEqual(item["distinct_nonempty_rd_block_sha256"],1030)
        self.assertEqual(len(item["duplicate_original_block_groups"]),1)
        self.assertEqual(item["duplicate_original_block_groups"][0]["original_bitmapnos"],[6042,6077])
        self.assertFalse(item["duplicate_original_block_groups"][0]["original_item_identity_same"])
        self.assertEqual(d["item_player_band_spr_frame_refs"],0)
        self.assertFalse(d["draw_selector_graphic_id_to_bitmapno_certified"])
        self.assertFalse(d["original_game_item_master_source_acquired"])
        self.assertFalse(d["copyrighted_game_pixels_published"])
if __name__=="__main__":unittest.main()
