"""PET19 original Taiwan v1 PC local item selection source and schema safeguards."""
import hashlib,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA="research/pets/PET-DETAIL-EVIDENCE19-TW10-NATIVE-ITEM-SELECT-COUNT-GATE-R1.json"
SCRIPT="tools/stoneage_pet_detail19_original_inventory_selection_replay.py"

def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def blob(p):
 b=(ROOT/p).read_bytes()
 return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

class PET19OriginalInventorySelect(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.d=read(DATA)
  x=importlib.util.spec_from_file_location("original_tw10_private19",ROOT/SCRIPT)
  cls.s=importlib.util.module_from_spec(x);x.loader.exec_module(cls.s)
 def test_original_source_identity_and_earlier_work(self):
  d=self.d;src=d["source"]
  self.assertEqual(src["archive_sha256"],self.s.ZIP_SHA)
  self.assertEqual(src["original_exe_sha256"],self.s.EXE_SHA)
  self.assertEqual(src["archive_bytes"],372626292)
  self.assertTrue(src["original_replay_executed_locally_and_passed"])
  self.assertFalse(src["original_executable_runtime_not_started"] is False)
  self.assertFalse(src["original_commercial_bytes_published"])
  for item in d["cross_source_boundary"].values():
   if isinstance(item,dict) and "git_blob" in item:
    self.assertEqual(blob(item["path"]),item["git_blob"])
  self.assertEqual(blob("docs/CURRENT-STATE.md"),d["cross_source_boundary"]["historical_current_state_git_blob_unchanged"])
 def test_three_sha_windows_and_independent_raw_native_checks(self):
  d=self.d;n=d["original_native_verified"]
  self.assertEqual(len(d["windows"]),3)
  for w in d["windows"]:
   self.assertEqual(self.s.WINDOWS[w["name"]],(int(w["start"],16),int(w["stop_exclusive"],16),w["sha256"]))
   self.assertEqual(w["byte_length"],int(w["stop_exclusive"],16)-int(w["start"],16))
  self.assertEqual((len(self.s.ASM),len(self.s.OPCODES)),(36,25))
  self.assertEqual((n["independent_objdump_instruction_anchors"],n["raw_instruction_opcode_checks"]),(36,25))
  self.assertEqual(self.s.OPCODES[0x42a7ec],"83fe05")
  self.assertEqual(self.s.OPCODES[0x42a910],"83fb02")
  self.assertEqual(self.s.OPCODES[0x42aa94],"83fd14")
 def test_true_client_local_selection_semantics_not_server_recipe(self):
  n=self.d["original_native_verified"]
  self.assertEqual(n["computed_item_record_stride_bytes"],156)
  self.assertEqual((5*8-1)*4,156)
  self.assertEqual(n["UI_state_record_stride_bytes"],32)
  self.assertEqual(n["bag_candidate_slot_indices"],[5,19])
  self.assertEqual((int(n["UI_state_end_exclusive"],16)-int(n["UI_state_first_address"],16))//32,15)
  self.assertEqual(n["bag_candidate_slot_count"],15)
  self.assertEqual(n["visible_slot_count"],20)
  self.assertEqual(n["selected_entry_count_cmp_2_va"],"0x42a910")
  self.assertEqual(n["selected_entries_below_2_branch_va"],"0x42a913")
  self.assertEqual(n["UI_transition_skip_target"],"0x42a988")
  self.assertTrue(n["local_selection_at_least_two_before_advance"])
  self.assertIsNone(n["original_item_flag_bit_2_semantics"])
  self.assertFalse(n["original_UI_any_stable_server_recipe_formula_proven"])
 def test_source_gates_and_continuity(self):
  g=self.d["cross_source_boundary"]
  self.assertTrue(g["client_local_selection_gate_NOT_server_recipe_minimum"])
  self.assertTrue(g["user_input_UI_local_state_NOT_network_packet"])
  for k in ("authentic_original_server_skill_master","authentic_original_server_W_message","actual_pet_crafting_success_or_loss_result"):
   self.assertIsNone(g[k])
  self.assertEqual(g["TW10_original_client_pet_dossiers_partial"],124)
  self.assertEqual(g["TW10_original_client_pet_dossiers_historical_full"],0)
  self.assertIsNone(g["overall_percent"])
  self.assertIn("PET-DETAIL19",(ROOT/"docs/pets/INDEX.md").read_text(encoding="utf-8"))
if __name__=="__main__":unittest.main()
