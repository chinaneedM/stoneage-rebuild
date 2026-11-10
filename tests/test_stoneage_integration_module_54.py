"""INTEGRATION54: reproduce source-bounded Giiru original DAT and TW1 strict pixel joins."""
import unittest,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P=R/"research/recovered/STONEAGE-INTEGRATION54-GIIRU-MINER-DAT-TW10-REAL-PIXELS-R1.json"
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+bytes([0])+b).hexdigest()
class T(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads(P.read_text(encoding="utf8"));cls.src={}
  for k,v in cls.r["source_git_blobs"].items():
   b=(R/v["path"]).read_bytes();assert blob(b)==v["sha"],k
   cls.src[k]=json.loads(b)
 def test_history(self):
  self.assertEqual(self.r["historical_current"]["blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
  self.assertEqual(self.r["historical_current"]["bytes"],2709173)
  self.assertFalse(self.r["historical_current"]["modified"])
 def test_private_original_source_custody(self):
  a=self.r["actual_private_replay"];self.assertEqual((a["quest12_zip"]["bytes"],a["quest12_zip"]["member_crc_pass"]),(113328,32))
  self.assertEqual(a["quest12_zip"]["sha256"],"d93aea416ea40a336e9c05a7cd851dbfc557916322f00152d91224f717c54cd9")
  self.assertNotEqual(a["quest12_zip"]["sha256"],self.src["q12"]["source_archive_sha256"])
  self.assertEqual(a["pet07_html"]["sha256"],self.src["p07"]["private_artifacts"]["catalog"]["sha256"])
  self.assertEqual(a["pet07_html"]["bytes"],self.src["p07"]["private_artifacts"]["catalog"]["bytes"])
  self.assertEqual(a["private_package"]["members_crc_pass"],10)
  self.assertTrue(a["private_package"]["Library_uploaded_then_retrieved_full_SHA_and_CRC_match"])
 def test_real_two_DATs_all_five_cells(self):
  self.assertEqual(self.r["original_two_DATs_five_source_cells_replayed"],self.src["q12"]["map_source_observations"])
  m=self.r["original_two_DATs_five_source_cells_replayed"]
  self.assertEqual([x["floor"] for x in m],[31805,31806])
  self.assertEqual(sum(len(x["source_points"]) for x in m),5)
  self.assertTrue(all(x["original_DAT_bytes"]==8+6*x["geometry"][0]*x["geometry"][1] for x in m))
  mid=next(x for x in m[0]["source_points"] if x["label"]=="miner_center")
  self.assertEqual((mid["xy"],mid["source_three_u16_values"]),([26,23],[5068,0,49157]))
 def test_original_miner_and_gate_source_identity(self):
  q=self.src["q12"]
  self.assertEqual(self.r["original_miner_create"],q["miner_create"][0])
  self.assertEqual(self.r["original_miner_and_gate_arg_literals"],q["other_original_controls"])
  self.assertEqual(self.r["original_miner_create"]["borncenter"],[26,23,1,1])
  self.assertIsNone(self.r["original_miner_create"]["borncorner"])
  self.assertEqual([x["sha256"] for x in self.r["original_QUEST12_source_files_reopened"]],[x["sha256"] for x in q["source_files"] if x["path"] in ("300/sb_bac.create","300/sb_bac.arg","genout/wpm_31805_22_4")])
  args={x["key"]:x["raw_value"] for x in self.r["original_miner_and_gate_arg_literals"]["300/sb_bac.arg"]}
  self.assertEqual((args["item"],args["enemyno"],args["steal"]),("2535","1004","1"))
 def test_TW1_graphic_group_exact_SPR_sha(self):
  g=self.r["TW10_original_100401_SPR_source_group"]
  self.assertEqual(g,next(x for x in self.src["p07"]["source_groups"] if x[0]==100401))
  a=next(x for x in self.src["p15"]["groups"] if x["graphic"]==100401)
  self.assertEqual((g[1],g[2]),(a["group_index"],a["segment_sha256"]))
  self.assertEqual((a["source_sequences"],a["frame_positions"],a["distinct_bitmaps"]),(104,496,344))
 def test_eight_real_original_PNG_receipts_have_exact_historical_hashes(self):
  got=self.r["TW10_PET07_actual_reopened_eight_original_bitmap_PNG_receipts"]
  want=[x for x in self.src["p07"]["source_actual_pixel_receipts"] if 82737<=x[0]<=82744]
  self.assertEqual(got,want)
  self.assertEqual([x[0] for x in got],list(range(82737,82745)))
  self.assertTrue(all(x[5]>0 and x[6]>0 and len(x[8])==64 for x in got))
  self.assertEqual(self.r["actual_private_replay"]["pet07_html"]["reopened_original_PNG_bitmap_ids"],list(range(82737,82745)))
 def test_strict_failure_is_not_retroactively_full_decode(self):
  x=self.r
  self.assertEqual(x["TW10_PET07_actual_strict_unrenderable_source_sequence"],next(a for a in self.src["p07"]["source_renderable_sequences_excluded"] if a["graphic"]==100401))
  self.assertEqual(x["TW10_PET07_unrenderable_original_RD"],next(a for a in self.src["p07"]["source_undecodable_actual_RD_blocks"] if a["bitmap"]==82729))
  self.assertEqual(x["TW10_PET07_actual_strict_unrenderable_source_sequence"]["original_frame_positions"],26)
  self.assertIn(82729,self.src["p15"]["bounded_bitmaps"])
  self.assertEqual(x["TW10_PET15_later_bounded_interpretation"]["status"],"NOT_RETROACTIVE_PET07_STRICT_LOSSLESS_RD_DECODE")
 def test_primary_alternate_template719_source_conflict(self):
  for f in ("enemybase.txt","enemybase2.txt"):
   old=[x for x in self.src["p10"]["source_rows"][f] if x[2]==100401]
   self.assertEqual(self.r["mixed25_alternative_original_template_rows_for_same_number"][f],[[x[0],x[1],x[2],x[3],x[16]] for x in old])
  self.assertEqual([x[1] for x in self.r["mixed25_alternative_original_template_rows_for_same_number"]["enemybase.txt"]],[500,544,713,719])
  self.assertEqual(self.r["exact_template_719_PETFLG_conflict"]["primary"],1)
  self.assertEqual(self.r["exact_template_719_PETFLG_conflict"]["alternative"],0)
 def test_rights_and_native_execution_guards(self):
  self.assertTrue(all(v is False for v in self.r["not_claims"].values()))
  self.assertEqual((self.r["summary"]["original_DATs_actually_reopened"],self.r["summary"]["original_source_cells_actually_replayed"],self.r["summary"]["real_previously_verified_sprite_PNG_bytes_reopened_and_sha_checked"]),(2,5,8))
  self.assertEqual(self.r["summary"]["original_sprite_RD_blocks_newly_decoded"],0)
  self.assertIsNone(self.r["overall_percent"])
  self.assertEqual((self.r["stage_A"],self.r["stage_B"],self.r["wiki"],self.r["R79"]),("7 PARTIAL + 2 OPEN","GATED","GATED","PAUSED_NON_BLOCKING"))
if __name__=="__main__":unittest.main()
