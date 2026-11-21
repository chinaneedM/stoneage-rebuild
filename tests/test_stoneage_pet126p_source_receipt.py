import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"research/recovered/STONEAGE-PET126P-CN50-ORIGINAL-ALBUM13-305X80-FILE-ACCESS-R1.json"

class PET126POriginalSourceProof(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads(DATA.read_text(encoding="utf-8"))
 def test_same_original_classic_pc_exe_and_source_replay(self):
  x=self.r
  self.assertEqual(x["source"]["bytes"],630784)
  self.assertEqual(x["source"]["sha256"],"5dbcc3fa276f9f245fb706bce957e9c3300d870df813889502b789b727e49c97")
  self.assertEqual(x["actual_source_replay"]["real_source_sha_check"],"success")
  self.assertFalse(x["source"]["source_executable_executed"])
  self.assertFalse(x["source"]["original_commercial_exe_or_album_bytes_published"])
 def test_all_305_original_keys_and_file_block_arithmetic(self):
  z=self.r["input_name_table"];n=self.r["original_native_source_path"]
  self.assertEqual((z["original_compiled_rows"],z["populated_names"],z["blank_slots"]),(362,305,57))
  self.assertEqual((z["first_i32_min"],z["first_i32_max"],z["populated_unique_raw_first_i32"]),(0,304,305))
  self.assertEqual(n["local_global_file_block_stride_dec"],24416)
  self.assertEqual(n["native_compiled_per_row_file_width_dec"],80)
  self.assertEqual(16+305*80,24416)
  self.assertEqual(n["last_record_relative_start_offset"],16+304*80)
  self.assertEqual(n["last_record_exclusive_end_offset"],24416)
  self.assertTrue(n["unique_key_range_fits_entire_candidate_block"])
  self.assertEqual(n["compiled_native_entry"],"0x430665")
  self.assertEqual(n["bounded_source_instruction_count"],83)
 def test_compiled_name_to_graphics_is_not_native_proven(self):
  x=self.r["grading"]
  self.assertEqual(x["actual_original_runtime_album_file_content"],"MISSING")
  self.assertEqual(x["compiled_name_to_spr_image_group"],"NOT_PROVEN")
  self.assertTrue(x["does_not_prove_exact_original_disk_header_or_all_records_present"])
  self.assertEqual(x["species_officially_released_new_count"],0)
  self.assertFalse(x["pet_closed"])
  self.assertEqual(x["year_2026"],"NOT_YEAR_AUDITED")
  self.assertIsNone(x["overall_percent"])
  self.assertTrue(x["no_mobile_or_paid_sources"])
  raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
  self.assertEqual(len(raw),2709173)
  self.assertEqual(hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest(),x["original_current_blob_unchanged"])

if __name__=="__main__":
 unittest.main()
