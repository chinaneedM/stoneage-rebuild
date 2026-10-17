"""Independent audit: never truncate historical ledgers while appending new research."""
import json, unittest
from pathlib import Path
from tools.stoneage_legacy_assistant_pet_coverage import ROOT,sha,MANIFEST,validate
R=ROOT/"research/recovered/STONEAGE-LEGACY-ASSISTANT-PET-COVERAGE-ARCHIVE-R1.json"
class Continuity(unittest.TestCase):
 def test_existing_full_prefixes(self):
  r=json.loads(R.read_text(encoding="utf-8"))
  self.assertEqual(len(r["historical_prefixes"]),5)
  for f in r["historical_prefixes"]:
   with self.subTest(f["path"]):
    raw=(ROOT/f["path"]).read_bytes()
    self.assertGreater(len(raw),f["bytes"])
    self.assertEqual(sha(raw[:f["bytes"]]),f["blob"])
 def test_source_run_and_restrictions(self):
  r=json.loads(R.read_text(encoding="utf-8"))
  self.assertEqual(r["source_tool_workflow_run"],{"id":39006252877,"conclusion":"SUCCESS","evidence_only":True})
  for k in ("complete_original_pet_catalog","complete_original_quests","all_legacy_cheats_catalogued","original_stage_a_acceptance_revoked","stage_b_production_started"):self.assertFalse(r[k])
  self.assertIn(r["archive_workflow"],("PENDING_NOT_CLAIMED","SUCCESS"))
  self.assertIn(r["main_integration"],("PENDING_NOT_CLAIMED","SUCCESS"))
  self.assertEqual(validate(json.loads(MANIFEST.read_text(encoding="utf-8")))["status"],"PASS")
 def test_ledger_new_evidence_has_version_guards(self):
  s=(ROOT/"docs/SOURCE-REGISTRY.md").read_text(encoding="utf-8")
  d=(ROOT/"docs/DESIGN-DECISIONS.md").read_text(encoding="utf-8")
  t=(ROOT/"docs/HISTORICAL-TIMELINE.md").read_text(encoding="utf-8")
  c=(ROOT/"docs/CURRENT-STATE.md").read_text(encoding="utf-8")
  self.assertIn("S01 2001-06-15",s);self.assertIn("S14 2026年",s)
  self.assertIn("## DD-025",d);self.assertIn("Classic StoneAge外挂/辅助工具",t)
  self.assertIn("PET-ASSET-GROWTH-CATALOG-MATRIX-02",c)
if __name__=="__main__":unittest.main()
