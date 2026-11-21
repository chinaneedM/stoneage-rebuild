import hashlib,json,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]
class PET126NSourceReceipt(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.x=json.loads((P/"research/recovered/STONEAGE-PET126N-CN50-ORIGINAL-80BYTE-RUNTIME-SLOT-SOURCE-R1.json").read_text(encoding="utf8"))
 def test_original_source_and_qualified_pc(self):
  x=self.x;self.assertEqual(x["source"]["exe_bytes"],630784)
  self.assertEqual(x["source"]["exe_sha256"],"5dbcc3fa276f9f245fb706bce957e9c3300d870df813889502b789b727e49c97")
  self.assertFalse(x["source"]["original_exe_executed"])
  self.assertEqual(x["source"]["actual_job_conclusion"],"success")
  self.assertEqual(x["source"]["synthetic_tests_conclusion"],"success")
 def test_compiled_362_vs_runtime_slot_80(self):
  x=self.x["source_verified"];self.assertEqual(x["compiled_table_rows"],362)
  self.assertEqual(x["count_global_init"],"mov DWORD PTR ds:0x332e4bc,0x16a")
  self.assertEqual(x["compile_table_row_stride"],28)
  self.assertEqual(x["runtime_record_stride"],80)
  self.assertEqual(x["status_offset_from_runtime_record_base"],76)
  self.assertEqual(x["compiled_table_pointer_file_positions"],[199700,200343,214772])
  self.assertEqual((x["state_field_exact_literal_references"],x["neighbor_fields_within_80_bytes_literal_references"]),(6,31))
 def test_nonpromotion_and_state_history(self):
  x=self.x;self.assertFalse(x["limits"]["same_version_graphic_selector_proven"])
  self.assertFalse(x["limits"]["matching_disk_adrn_record_layout_proven"])
  self.assertFalse(x["limits"]["program_runtime_exec_verified"])
  self.assertEqual(x["limits"]["official_pet_species_new_confirmed"],0)
  self.assertIsNone(x["limits"]["overall_percent"])
  self.assertFalse(x["limits"]["mobile_included"])
  data=(P/"docs/CURRENT-STATE.md").read_bytes()
  self.assertEqual(len(data),2709173)
  self.assertEqual(hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest(),x["limits"]["source_state_git_blob_unchanged"])
if __name__=="__main__":unittest.main()
