"""Archive source-comparison outputs without retroactively changing evidence."""
import json,unittest
from tools.stoneage_early_ui_bitmap_range_audit import audit,ROOT,gitblob
RECORD=ROOT/"research/recovered/STONEAGE-EARLY-VISUAL-ID-RANGES-VERIFIED-R1.json"
class VisualArchive(unittest.TestCase):
 def test_exact_report(self):
  r=json.loads(RECORD.read_text(encoding="utf-8"))
  self.assertEqual(audit(),r["verified_range_report"])
  self.assertEqual(r["verified_action"],{"run":39025092843,"job":117374413945,"conclusion":"SUCCESS"})
  self.assertEqual(r["workflow_failure"]["result"],"failure")
  self.assertEqual(r["workflow_failure"]["run"],39025014067)
 def test_prefixes(self):
  r=json.loads(RECORD.read_text(encoding="utf-8"))
  self.assertEqual(len(r["historical_prefixes"]),4)
  for p in r["historical_prefixes"]:
   with self.subTest(p["path"]):
    data=(ROOT/p["path"]).read_bytes()
    self.assertGreater(len(data),p["bytes"])
    self.assertEqual(gitblob(data[:p["bytes"]]),p["blob"])
 def test_keep_unknowns(self):
  r=json.loads(RECORD.read_text(encoding="utf-8"))
  for key in ("same_build_original_rendering_verified","original_login_screen_recovered","original_character_images_bound_to_char_ids","original_pet_species_ids_bound_to_portraits","old_new_version_merge_allowed","original_copyrighted_bitmap_payload_committed","all_classified_original_pet_images_complete"):
   self.assertFalse(r[key])
  self.assertIsNone(r["overall_restoration_percent"])
  self.assertEqual(r["next"],"WORLD-NPC-QUEST-SOURCE-JOIN-01")
  self.assertIn(r["archive_ci"],("PENDING_NOT_CLAIMED","SUCCESS"))
  self.assertIn(r["main_ci"],("PENDING_NOT_CLAIMED","SUCCESS"))
if __name__=="__main__":unittest.main()
