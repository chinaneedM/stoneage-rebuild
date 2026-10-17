"""Five exact original Git prefixes protected independently of source-field validator."""
import unittest,json
from tools.stoneage_preproduction_archive import ROOT,PATH,validate,gitblob
R=ROOT/"research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-ACCEPTANCE-R1.json"
class Archive(unittest.TestCase):
 def test_all_original_long_documents_preserved(self):
  p=json.loads(R.read_text(encoding="utf-8"))
  self.assertEqual(len(p["historical_prefixes"]),4)
  for x in p["historical_prefixes"]:
   with self.subTest(x["path"]):
    b=(ROOT/x["path"]).read_bytes()
    self.assertGreater(len(b),x["bytes"])
    self.assertEqual(gitblob(b[:x["bytes"]]),x["blob"])
 def test_source_run_real_not_preclaimed_main(self):
  p=json.loads(R.read_text(encoding="utf-8"))
  self.assertEqual(p["source_workflow"],{"run":39007115468,"result":"SUCCESS"})
  self.assertIn(p["archive_ci"],("PENDING_NOT_CLAIMED","SUCCESS"))
  self.assertIn(p["main_ci"],("PENDING_NOT_CLAIMED","SUCCESS"))
  for k in ("new_original_server_payload","original_ui_runtime_restored","all_pets_quests_complete","all_helper_exploit_functions_reproduced","new_game_started","website_built"):self.assertFalse(p[k])
  self.assertEqual(validate(json.loads(PATH.read_text(encoding="utf-8")))["status"],"PASS")
 def test_new_priority_is_in_all_governance_text(self):
  for path in ("docs/CURRENT-STATE.md","docs/DESIGN-DECISIONS.md","docs/RESTORATION-ROADMAP-R2.md"):
   text=(ROOT/path).read_text(encoding="utf-8")
   self.assertIn("PET-ASSET-GROWTH-CATALOG-MATRIX-02",text)
  text=(ROOT/"docs/SOURCE-REGISTRY.md").read_text(encoding="utf-8")
  self.assertIn("WEB_QUEST_INDEX",text)
  self.assertIn("WEB_PET_INDEX",text)
if __name__=="__main__":unittest.main()
