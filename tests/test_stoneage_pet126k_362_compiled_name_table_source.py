"""PET126K directly verified CN5 PC name table; names never imply issued species."""
import hashlib,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(name):return json.loads((R/"research/recovered"/name).read_text(encoding="utf-8"))
class Pet126KTable(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=read("STONEAGE-PET126K-CN50-ORIGINAL-362-NAMED-SLOTS-TW10-CROSSWALK-R1.json")
  cls.src=read("STONEAGE-STONEAGE5-REAL-CAB-PAYLOAD-R1.json")
  cls.tw=read("STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")
 def test_actual_source_hash_identity_and_uncertified_pressing(self):
  a=self.e["source"]; files={x["name"]:(x["size"],x["sha256"]) for x in self.src["files"]["inventory"]}
  self.assertEqual(files[a["program"]],(a["program_bytes"],a["program_sha256"]))
  self.assertEqual(files[a["launcher"]],(a["launcher_bytes"],a["launcher_sha256"]))
  self.assertEqual(a["cab_sha256"],self.src["source"]["cab_sha256"])
  self.assertFalse(self.src["boundaries"]["official_clean_proven"])
  self.assertTrue(a["not_new_unique_client_build"])
  self.assertEqual(a["new_original_source_program_bytes_rehashed"],856064)
 def test_362_slot_full_span_and_57_old_exact_blanks(self):
  t=self.e["original_5_0_typed_client_name_table"];a=t["first_181"];b=t["second_181"]
  self.assertEqual((t["rows"],t["row_stride_bytes"],t["filled"],t["empty"]),(362,28,305,57))
  self.assertEqual((a["filled"],a["empty"],b["filled"],b["empty"]),(124,57,181,0))
  self.assertEqual(t["distinct_printed_names"],305)
  self.assertEqual(a["same_slot_literal_exact_unicode_name_matches"],49)
  self.assertTrue(a["exactly_same_TW10_blank_positions"])
  blanks=sorted(n-self.tw["table"]["first_graphic"] for n in self.tw["table"]["placeholder_graphics"])
  self.assertEqual(a["blank_slot_ordinals"],blanks)
  self.assertEqual(len(self.tw["records"]),124)
  self.assertEqual(len(a["exact_name_examples"]),10)
 def test_no_live_species_proof_and_original_CURRENT_preservation(self):
  x=self.e
  self.assertEqual(x["active_module"],"PET")
  self.assertTrue(all(x["guard"].values()))
  self.assertEqual(x["new_qualifying_official_species"],0)
  self.assertEqual(x["pet_status"],"SOURCE_BOUNDED_PARTIAL")
  self.assertFalse(x["source_bounded_closed"])
  self.assertEqual(x["year_2026"],"NOT_YEAR_AUDITED")
  self.assertIsNone(x["overall_percent"])
  raw=(R/"docs/CURRENT-STATE.md").read_bytes()
  self.assertEqual(len(raw),2709173)
  self.assertEqual(hashlib.sha1(b"blob "+str(len(raw)).encode()+bytes([0])+raw).hexdigest(),x["baseline"]["current_blob"])
if __name__=="__main__":unittest.main()
