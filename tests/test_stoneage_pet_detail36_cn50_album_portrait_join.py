"""PET36: retain the exact original-source-derived 305-name -> RD projection."""
import json
import unittest
from pathlib import Path
from tools.stoneage_pet_detail36_cn50_album_portrait_join import audit

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/pets/PET-DETAIL-EVIDENCE36-CN50-ALBUM-ADRN-RD-PROJECTION-R1.json"
NAMES={
 "葛雷基欧":234391,"葛雷洛比":234389,"葛雷吉鲁":234390,
 "葛雷马恩":234392,"艾迪希洛":284530,"蒙奇":284529,"菲奇亚":284528
}

class SourceJoin(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=audit()
  cls.expected=json.loads(REPORT.read_text(encoding="utf-8"))
 def test_permanent_report_reproduces_exactly_from_source_pins(self):
  self.assertEqual(self.a,self.expected)
 def test_all_named_same_saved_cab_adrn_last_projection(self):
  a=self.a
  self.assertEqual((a["counts"]["all_album_slots"],a["counts"]["named_album_rows"]),(362,305))
  self.assertEqual((a["counts"]["distinct_named_aliases"],a["counts"]["named_aliases_with_last_record_projection"]),(305,305))
  self.assertEqual(a["counts"]["named_aliases_without_last_record_projection"],0)
  self.assertEqual(len({r["last_projected_physical_rd_bitmapno"] for r in a["records"]}),305)
  for r in a["records"]:
   self.assertTrue(r["same_CAB_ADRN_last_record_projection_present"])
   self.assertEqual((r["same_CAB_rd_width"],r["same_CAB_rd_height"]),(96,104))
   self.assertEqual(len(r["same_CAB_rd_block_sha256"]),64)
   self.assertFalse(r["actual_native_renderer_selection_verified"])
   self.assertFalse(r["duplicate_original_ADRN_candidates_ruled_out"])
   self.assertFalse(r["same_build_original_server_pet_id_verified"])
   self.assertFalse(r["historical_official_live_release_verified_by_this_join"])
 def test_seven_early_late_historical_pc_name_art_candidates(self):
  rows={r["client_compiled_name"]:r for r in self.a["records"]}
  for name,bitmap in NAMES.items():
   with self.subTest(name=name):
    self.assertEqual(rows[name]["last_projected_physical_rd_bitmapno"],bitmap)
    self.assertEqual(self.a["seven_historical_name_source_checks"][name],rows[name])
 def test_duplicate_original_alias_negative_control_and_pet_egg(self):
  aliases={r["source_compiled_alias_u32"]:r["last_projected_physical_rd_bitmapno"] for r in self.a["records"]}
  self.assertEqual([aliases[k] for k in (28085,28086,28087,28088)],
                   [126222,126223,126224,126225])
  self.assertTrue(self.a["known_collision_negative_control"]["one_record_projection_is_not_original_full_candidate_list"])
  self.assertTrue(self.a["known_collision_negative_control"]["last_in_ADRN_is_not_proven_game_display_choice"])
  self.assertFalse(next(r for r in self.a["records"] if r["client_compiled_name"]=="宠物蛋")["historical_official_live_release_verified_by_this_join"])
 def test_provenance_and_scope(self):
  a=self.a
  self.assertEqual((a["active_module"],a["scope"]),("PET","CLASSIC_PC_ONLY"))
  for k in ("saved_CAB_independently_certified_official_distribution",
            "same_build_native_selector_verified","all_original_ADRN_alias_candidates_enumerated",
            "album_name_is_an_actually_issued_live_pet","original_RD_pixels_recovered_in_this_audit"):
   self.assertFalse(a["claims"][k])
  self.assertFalse(a["source_safety"]["raw_commercial_images_binaries_published"])
  self.assertIsNone(a["source_safety"]["overall_percent"])
  self.assertEqual(a["counts"]["same_build_official_server_pet_ids_newly_verified"],0)
  self.assertEqual(a["counts"]["live_pet_issuance_newly_verified"],0)

if __name__=="__main__":
 unittest.main()
