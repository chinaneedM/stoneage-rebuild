"""PET-DETAIL18 original PC native ID/operation label positive and negative guards."""
import hashlib,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA="research/pets/PET-DETAIL-EVIDENCE18-TW10-NATIVE-ID200-201-UI-LABEL-BRIDGE-R1.json"
SCRIPT="tools/stoneage_pet_detail18_tw10_native_ui_label_replay.py"
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def gitblob(p):
 b=(ROOT/p).read_bytes()
 return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
class OriginalIDLabel(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=read(DATA)
  s=importlib.util.spec_from_file_location("pet18_replay",ROOT/SCRIPT)
  cls.source=importlib.util.module_from_spec(s);s.loader.exec_module(cls.source)
 def test_original_source_and_unmodified_prior_work(self):
  r=self.r;s=r["source"]
  self.assertEqual(s["original_zip_sha256"],self.source.ZIP_SHA)
  self.assertEqual(s["exe_sha256"],self.source.EXE_SHA)
  self.assertTrue(s["original_zip_exe_reopened_and_verified_this_turn"])
  self.assertFalse(s["original_asset_bytes_published"])
  for p in r["pinned_prior"]:self.assertEqual(gitblob(p["path"]),p["git_blob"])
  self.assertEqual(gitblob("docs/CURRENT-STATE.md"),r["limits"]["current_historical_state_blob_unchanged"])
 def test_native_windows_opcode_and_CP950_anchors(self):
  r=self.r
  self.assertEqual(len(r["source_windows"]),3)
  self.assertEqual(len(self.source.WINDOWS),3)
  for w in r["source_windows"]:
   self.assertEqual(self.source.WINDOWS[w["name"]],(int(w["start_va"],16),int(w["end_exclusive_va"],16),w["sha256"]))
   self.assertEqual(w["length"],int(w["end_exclusive_va"],16)-int(w["start_va"],16))
  self.assertEqual(len(self.source.OPCODES),22)
  self.assertEqual(len(self.source.ASM),12)
  self.assertEqual(len(self.source.LABELS),2)
  self.assertEqual(r["private_audit_checks"]["original_objdump_instruction_anchors"],26)
  self.assertEqual(r["public_replay_checks"]["original_objdump_instruction_anchors"],12)
  self.assertEqual(self.source.OPCODES[0x42a85a],"68c9000000")
  self.assertEqual(self.source.OPCODES[0x42a883],"68c8000000")
 def test_verified_client_UI_labels_not_server_master_names(self):
  row={x["client_checked_skill_id"]:x for x in self.r["native_client"]["verified_ID_to_UI_operation"]}
  self.assertEqual((row[200]["client_local_state"],row[200]["original_CP950_operation_literal"]),(1,"合成"))
  self.assertEqual((row[201]["client_local_state"],row[201]["original_CP950_operation_literal"]),(2,"料理"))
  for a in self.source.LABELS:
   x=row[a[0]]
   self.assertEqual((a[1],a[2],a[3],a[4],a[5]),(x["original_CP950_operation_literal"],x["client_local_state"],int(x["string_address"],16),int(x["literal_pointer_instruction_va"],16),x["literal_with_4_nul_sha256"]))
  g=self.r["limits"]
  self.assertTrue(g["verified_client_UI_operation_not_original_official_server_skill_name"])
  self.assertTrue(g["native_200_UI_label_合成_not_加工"])
  for key in ("original_server_skill_name_200","original_server_skill_name_201","original_server_skill_effects","original_official_pet_birth_skills","original_server_PetSkill_master","original_real_W_packet"):self.assertIsNone(g[key])
  self.assertFalse(g["original_client_runtime_UI_executed"])
  self.assertEqual(g["TW10_partial_pet_profiles"],124)
  self.assertEqual(g["TW10_historically_fully_accepted"],0)
  self.assertIsNone(g["overall_percent"])
  self.assertIn("PET-DETAIL18",(ROOT/"docs/pets/INDEX.md").read_text(encoding="utf-8"))
if __name__=="__main__":unittest.main()
