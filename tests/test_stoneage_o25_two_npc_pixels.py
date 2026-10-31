"""O25 original-resource source-derived guard mutations; no private RD in public CI."""
import copy,json,unittest
from tools.stoneage_o25_two_npc_pixels import REPORT,validate
class O25OriginalTwoNpcSourceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.o=json.loads(REPORT.read_text(encoding="utf-8"))
 def test_actual_two_original_aliases(self):
  self.assertEqual(validate(self.o),{"original_RD_blocks":4,"source_NPCs":2,"distinct_alias_candidates":2,"false_literal_physical_controls":2})
 def test_source_pins_and_historic_period(self):
  for k,v in [("TW10_P3H_zip",0),("TW10_ADRN",0),("TW10_REAL",0),("TW10_Palet1",0),("R3_observation_zip",0),("mixed25_ADRN",0)]:
   with self.subTest(key=k):
    d=copy.deepcopy(self.o);d["originals"][k]["bytes"]=v
    with self.assertRaises(ValueError):validate(d)
  d=copy.deepcopy(self.o);d["source_crossversion"]="OFFICIAL_TW10_NPC";self.assertRaises(ValueError,validate,d)
 def test_one_pixel_record_and_paired_comparator_mutations(self):
  for index in (0,1):
   for k,bad in [("alias",999),("physical",9999),("rd_bytes",0),("width",0),("record_sha","0"*64),("rd_sha","0"*64),("index_sha","0"*64),("rgba_sha","0"*64),("png_sha","0"*64),("control_rd_sha","0"*64),("control_index_sha","0"*64),("control_png_sha","0"*64),("control_physical",999)]:
    with self.subTest(index=index,key=k):
     d=copy.deepcopy(self.o);d["two_aliases"][index][k]=bad
     with self.assertRaises(ValueError):validate(d)
 def test_client_and_same_build_negative_claims(self):
  for k,v in self.o["proofs"].items():
   with self.subTest(key=k):
    d=copy.deepcopy(self.o);d["proofs"][k]=1 if v is None else not v
    with self.assertRaises(ValueError):validate(d)
  d=copy.deepcopy(self.o);d["private_archive"]["sha256"]="0"*64
  self.assertRaises(ValueError,validate,d)
if __name__=="__main__":unittest.main()
