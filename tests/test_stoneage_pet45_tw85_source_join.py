"""PET45: archive-invariant and no-official-promotion guards."""
import json
import unittest
from tools import stoneage_pet45_tw85_rd_index_coverage as p
class TestPet45(unittest.TestCase):
    def test_source_replay_and_evidence_limits(self):
        d=p.calculate()
        s=d["summary"]
        self.assertEqual((len(d["candidate_groups"]),s["original_physical_SPR_groups"]),(412,416))
        self.assertEqual((s["full_SPR_segment_exact_CN50_physical_groups"],s["unmatched_CN50_original_TW85_physical_groups"]),(214,202))
        self.assertEqual((s["frame_occurrences"],s["mapped_frames"],s["sentinel_frames"]),(197680,197678,2))
        self.assertEqual((s["missing_frames"],s["multiple_same_rd_frames"],s["multiple_different_rd_frames"]),(0,0,0))
        self.assertEqual((s["distinct_bitmap_ids"],s["distinct_mapped_rd_contents"],s["raw_sound_word_occurrences"]),(133914,132695,11714))
        self.assertEqual(s["duplicate_numeric_original_groups"],{"101866":3,"101990":2,"101991":2})
        self.assertEqual(len(d["TW1_six_without_qualified_album_names"]),6)
        self.assertEqual(len(d["four_carriers_index_absent_community_candidates"]),56)
        self.assertFalse(any(d["guardrails"].values()))
        self.assertFalse(d["same_carrier_file_inventory_name_scan"]["executable_content_read_now"])
        self.assertEqual(d["same_carrier_file_inventory_name_scan"]["explicit_pet_enemy_skill_like_filenames"],[])
        self.assertEqual((s["new_same_build_named_pets"],s["new_official_live_released_pets"],s["new_original_RD_pixels_decoded"]),(0,0,0))
        self.assertIsNone(s["historical_official_species_total"])
        self.assertTrue(all(not r["confirmed_official_live_pet_release"] and r["same_build_original_pet_name"] is None for r in d["candidate_groups"]))
        self.assertEqual(d["current_state_git_blob_preserved"],"c89e0e33537990aa2132b47c40fef49a985a935c")
    def test_artifact_exact_match(self):
        expected=json.dumps(p.calculate(),ensure_ascii=False,sort_keys=True,indent=2)+"\n"
        self.assertEqual(p.OUTPUT.read_text(encoding="utf-8"),expected)
        self.assertEqual(p.ROOT.joinpath("docs/STONEAGE-PET-CHRONOLOGICAL-RESTORATION-ORDER-R1.md").read_text(encoding="utf-8").count("## PET45 2026-11-16｜台湾8.5保存包412候选图号与197,680帧原RD索引覆盖"),1)
        self.assertEqual(p.ROOT.joinpath("research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json").read_text(encoding="utf-8").count('"PET45-TW85-SAME-CARRIER-SPR-RD-20261116"'),2)
if __name__=="__main__":
    unittest.main()
