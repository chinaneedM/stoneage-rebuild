"""PET126K synthetic scanner and pinned original-source regression; no commercial data."""
import json
import struct
import unittest
from pathlib import Path
from tools.stoneage_pet126k_cn50_original_exe_probe import EXPECTED, text_hits,parse_row,table_candidates,aligned_region_metadata
ROOT=Path(__file__).resolve().parents[1]
class PET126KSourceBoundary(unittest.TestCase):
 def test_synthetic_pet_name_in_valid_rows(self):
  name="烏力"
  encoded=name.encode("cp950")
  row=struct.pack("<i20sI",7,encoded+bytes(20-len(encoded)),28001)
  raw=b"HEADER"+row*12+b"\0TAIL"
  hits=text_hits(raw,[name],"cp950")
  self.assertEqual(len(hits),12)
  tables=table_candidates(raw,"cp950")
  self.assertEqual(len(tables),1)
  self.assertEqual(tables[0]["file_offset"],6)
  self.assertEqual(tables[0]["rows"],12)
  self.assertFalse(tables[0]["native_pet_id_or_release_proven"])
 def test_simplified_empty_rows_and_full_362_span(self):
  named="烏力".encode("gb18030")
  good=struct.pack("<i20sI",5,named+bytes(20-len(named)),28001)
  blank="无".encode("gb18030")
  empty=struct.pack("<i20sI",-1,blank+bytes(20-len(blank)),0)
  buf=(good+empty)*181
  self.assertEqual(len(buf),362*28)
  result=aligned_region_metadata(buf,0,362,"gb18030")
  self.assertTrue(result["is_whole_region_decodable"])
  self.assertEqual(result["counts"],{"populated":181,"empty":181,"unparsed":0})
  tables=table_candidates(buf,"gb18030")
  self.assertEqual(len(tables),1)
  self.assertEqual(tables[0]["rows"],362)
 def test_malformed_not_promoted(self):
  bad=struct.pack("<i20sI",7,"寵物".encode("cp950")+bytes(16),0)
  self.assertIsNone(parse_row(bad,0,"cp950"))
  self.assertEqual(table_candidates(bytes(1000),"cp950"),[])
 def test_pinned_EXE_file_hashes_and_unqualified_pressing(self):
  data=json.loads((ROOT/"research/recovered/STONEAGE-STONEAGE5-REAL-CAB-PAYLOAD-R1.json").read_text(encoding="utf-8"))
  self.assertEqual(data["files"]["count"],413)
  found={x["name"]:(x["size"],x["sha256"]) for x in data["files"]["inventory"]}
  for k,v in EXPECTED.items():self.assertEqual(found[k],v)
  self.assertFalse(data["boundaries"]["official_clean_proven"])
  self.assertFalse(data["boundaries"]["pet_quest_entity_identity_proven"])
  self.assertEqual(sum(x[0] for x in EXPECTED.values()),856064)
if __name__=="__main__":unittest.main()
