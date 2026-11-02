import copy,json,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"research/recovered"
def check(x,prior):
 assert x["schema"]=="stoneage.char03.tw1_101_NPC_like_original_pixel_receipt.r1"
 assert x["baseline"]["unchanged_current_state_blob"]=="20050acf279a01555ab06a381dfcdc936bd381a6"
 rows=sorted(prior["rows"],key=lambda z:z["bitmapno"])
 assert [r["bitmapno"] for r in rows]==list(range(5846,5947))
 h=2166136261
 for byte in "".join(str(r["bitmapno"])+":"+r["rd_block_sha256"]+"\n" for r in rows).encode():
  h=((h^byte)*16777619)&0xffffffff
 assert f"{h:08x}"==x["R99_source"]["sort_by_bitmap_number_and_source_rd_sha_FNV1A32"]=="e06ffcee"
 assert x["R99_source"]["source_first_RD_sha256"]==rows[0]["rd_block_sha256"]
 assert x["R99_source"]["source_last_RD_sha256"]==rows[-1]["rd_block_sha256"]
 a=x["observed"]
 assert all(a[k]==101 for k in ("original_ADRN_records_uniquely_located","original_REAL_RD_source_blocks_read","strict_original_RD_pixel_decoded","prior_R99_RD_sha_matches","local_chromium_images_loaded_palette_1","local_chromium_images_loaded_palette_0"))
 assert a["original_RD_failures"]==a["local_JS_errors"]==a["local_external_requests"]==0
 assert a["original_SAP_RGB_candidates"]==2
 assert a["visible_objects_include_nonhuman_props"] is True
 assert all(v is False for k,v in x["not_proven"].items() if k!="total_restoration_percent")
 assert x["not_proven"]["total_restoration_percent"] is None
 assert all(z["public_git"] is False for z in x["private_artifacts"].values())
 assert x["next"].startswith("CHARACTER_NPC_MODULE_04_")
class CHAR03(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.obj=json.loads((P/"STONEAGE-CHARACTER-NPC-MODULE-03-TW1-101-STATIC-RD-RECEIPT-R1.json").read_text())
  cls.prior=json.loads((P/"STONEAGE-TW10-NPC-STATIC-RESOURCE-JOIN-R99.json").read_text())
 def test_actual_source_metadata(self):check(self.obj,self.prior)
 def test_no_fake_official_NPC_count(self):
  x=copy.deepcopy(self.obj);x["not_proven"]["official_101_individual_NPCs"]=True
  with self.assertRaises(AssertionError):check(x,self.prior)
 def test_no_hypothetical_100_pixels(self):
  x=copy.deepcopy(self.obj);x["observed"]["strict_original_RD_pixel_decoded"]=100
  with self.assertRaises(AssertionError):check(x,self.prior)
 def test_no_publishing_copyrighted_pixels(self):
  x=copy.deepcopy(self.obj);x["private_artifacts"]["contact_sheet"]["public_git"]=True
  with self.assertRaises(AssertionError):check(x,self.prior)
if __name__=="__main__":unittest.main()
