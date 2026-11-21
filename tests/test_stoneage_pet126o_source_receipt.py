import hashlib,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class PET126O(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=json.loads((R/"research/recovered/STONEAGE-PET126O-CN50-ORIGINAL-ALBUM13-LOCAL-HELPERS-R1.json").read_text(encoding="utf8"))
 def test_same_original_exe_source_and_compiled_helpers(self):
  s=self.e["source"]
  self.assertEqual(s["program_bytes"],630784)
  self.assertEqual(s["program_sha256"],"5dbcc3fa276f9f245fb706bce957e9c3300d870df813889502b789b727e49c97")
  self.assertFalse(s["original_program_executed"])
  a=self.e["helper_0x45f560"];b=self.e["helper_0x430665"]
  self.assertEqual(a["direct_call_sites_in_same_exe"],232)
  self.assertEqual(b["direct_call_sites_in_same_exe"],5)
  self.assertTrue(a["verified_character_copy_pattern"])
  self.assertFalse(a["graphical_rendering_function_proven"])
 def test_real_local_album_filename_not_runtime_admitted(self):
  f=self.e["helper_0x430665"]["original_local_file"]
  self.assertEqual(f["literal_path"],"data\\album_13.dat")
  self.assertEqual(f["literal_mode"],"r+b")
  self.assertTrue(f["file_backed_literal"])
  self.assertTrue(f["call_target_known_as_fopen_not_yet_independently_decoded"])
  self.assertTrue(self.e["helper_0x430665"]["local_album_file_not_present_in_413_install_member_names"])
  self.assertFalse(self.e["helper_0x430665"]["original_file_currently_read_or_created_in_runtime_not_proven"] is False)
 def test_zero_pet_promotion_and_preserve_original_current(self):
  c=self.e["qualified_conclusions"]
  self.assertEqual(c["official_live_pet_issuance_confirmed"],0)
  self.assertFalse(c["graphical_data_selector_proven"])
  self.assertFalse(c["pet_module_closed"])
  self.assertIsNone(c["overall_percent"])
  x=(R/"docs/CURRENT-STATE.md").read_bytes()
  self.assertEqual(len(x),2709173)
  self.assertEqual(hashlib.sha1(b"blob "+str(len(x)).encode()+b"\0"+x).hexdigest(),c["original_current_blob_unchanged"])
if __name__=="__main__":unittest.main()
