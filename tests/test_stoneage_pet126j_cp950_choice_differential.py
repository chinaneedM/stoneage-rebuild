"""PET126J preserves earlier EXE-literal evidence without claiming new native gameplay."""
import hashlib
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
def data(s):return json.loads((ROOT/"research/recovered"/s).read_text(encoding="utf-8"))
class Pet126JCp950SourceOnly(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.x=data("STONEAGE-PET126J-TW10-CP950-PET-CHOICE-DIFFERENTIAL-R1.json")
  cls.d=data("STONEAGE-PET126D-TW10-CLIENT-CAPTURE-FIVE-SLOT-STATIC-R1.json")
  cls.e=data("STONEAGE-PET126E-TW10-K-STATUS-CAPTURE-STATIC-R1.json")
 def test_same_original_binary_not_new_client(self):
  x=self.x
  self.assertEqual(x["source"]["original_exe_sha256"],self.d["source"]["pe_member_sha256"])
  self.assertEqual(x["source"]["original_exe_sha256"],self.e["original_source"]["exe_sha256"])
  self.assertEqual(x["source"]["original_client_carrier_sha256"],self.d["source"]["archive_sha256"])
  self.assertTrue(x["source"]["original_binary_not_reaccessed_this_work_unit"])
  self.assertFalse(x["source"]["original_exe_uploaded_publicly"])
  self.assertEqual(x["difference"]["new_original_client_bytes"],0)
  self.assertEqual(x["difference"]["new_official_pet_species"],0)
 def test_complete_9_short_literals_have_10_positions_exact_cp950_digest(self):
  x=self.x
  rows=x["exact_source_rows"]
  self.assertEqual(len(rows),9)
  self.assertEqual(sum(len(r["offsets"]) for r in rows),10)
  self.assertEqual(sum(r["already_main_pet126d_xref"] for r in rows),7)
  self.assertEqual(sum(r["is_choice_prompt_static_delta"] for r in rows),2)
  for row in rows:
   encoded=row["text"].encode("cp950","strict")
   self.assertEqual(len(encoded),row["byte_length"])
   self.assertEqual(hashlib.sha256(encoded).hexdigest(),row["cp950_literal_sha256"])
   self.assertEqual(len(row["offsets"]),row["occurrence_count"])
   self.assertTrue(all(0<=n<=x["source"]["original_exe_size"]-len(encoded) for n in row["offsets"]))
   self.assertIsNone(row["species_id"])
   self.assertFalse(row["original_runtime_action_verified"])
 def test_substring_is_not_a_second_UI_action(self):
  x=self.x
  rows={r["id"]:r for r in x["exact_source_rows"]}
  self.assertEqual(rows["pet_choice_prompt"]["offsets"],[366255,366334])
  self.assertEqual(rows["pet_or_teammate_prompt"]["offsets"],[366334])
  self.assertTrue(rows["pet_or_teammate_prompt"]["text"].startswith(rows["pet_choice_prompt"]["text"]))
  self.assertTrue(x["substring_overlap"]["overlap_is_not_two_independent_UI_ACTIONS"])
  existing={p["file_offset"] for p in self.d["other_pet_ui_literal_xrefs"]}
  self.assertEqual(existing,{352068,352128,352180,378044,379308})
  self.assertEqual(int(self.d["capture_gate"]["label_vas"][0],16)-0x400000,352000)
  self.assertEqual(int(self.d["capture_gate"]["label_vas"][1],16)-0x400000,352008)
 def test_scope_gates_and_untouched_original_CURRENT(self):
  x=self.x
  self.assertTrue(all(x["negative_controls"].values()))
  self.assertEqual(x["active_module"],"PET")
  self.assertEqual(x["preserved_gate"]["year_2026"],"NOT_YEAR_AUDITED")
  self.assertFalse(x["preserved_gate"]["source_bounded_closed"])
  self.assertIsNone(x["preserved_gate"]["overall_completion_percent"])
  c=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
  self.assertEqual(len(c),2709173)
  self.assertEqual(hashlib.sha1(b"blob "+str(len(c)).encode()+bytes([0])+c).hexdigest(),x["baseline"]["original_current_blob"])
if __name__=="__main__":unittest.main()
