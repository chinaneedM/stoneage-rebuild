"""PET46: require source-exact native TW1 album name to old PET07 visual SPR."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"research/recovered"
def load(s):return json.loads((BASE/s).read_text(encoding="utf-8"))
class PET46(unittest.TestCase):
 def test_exact_original_same_client_join(self):
  out=load("STONEAGE-PET46-TW1-ALBUM-NAME-2D-CROSSWALK-R1.json")
  p7=load("STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json")
  p39=load("STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")
  self.assertEqual(out["schema"],"stoneage.pet46.tw1_retail_album_same_source_private_2d_crosswalk.r1")
  self.assertEqual((out["source_pins"][0]["git_blob"],out["source_pins"][1]["git_blob"]),("0b5f81b41a642025ab53a12884638fdee887470e","1aada81d7314769bf683b816cc5a8762c3bd9400"))
  records={x["graphic_number"]:x for x in out["candidate_records"]}
  names={x["graphic_number"]:x for x in p39["records"]}
  self.assertEqual((len(records),len(names)),(130,124))
  for source in p7["source_groups"]:
   num,index,sha,anims,frames,actions,bitmap_count=source
   rec=records[num]
   self.assertEqual((rec["pet07_original_SPR_index"],rec["pet07_original_whole_SPR_sha256"]),(index,sha))
   self.assertEqual((rec["pet07_source_total_animations"],rec["pet07_selected_source_frame_occurrences"],rec["pet07_selected_original_actions"],rec["pet07_selected_distinct_bitmap_ids"]),(anims,frames,actions,bitmap_count))
   name=names.get(num)
   if name:
    self.assertEqual((index,sha),(name["spr_group_index"],name["spr_original_segment_sha256"]))
    self.assertEqual((rec["client_original_album_name"],rec["client_original_album_row_sha256"],rec["client_original_album_row_file_offset"]),(name["name_as_written"],name["source_row_sha256"],name["source_file_offset"]))
   else:
    self.assertIsNone(rec["client_original_album_name"])
    self.assertIsNone(rec["client_original_album_row_sha256"])
   self.assertFalse(rec["official_live_pet_proven"])
   self.assertFalse(rec["original_pixels_newly_decoded_in_this_work"])
  self.assertEqual(out["original_source_SPR_without_album_names"],[100015,100018,100401,100432,100451,100454])
  self.assertEqual({x["graphic_number"] for x in out["candidate_records"] if x["client_original_album_explicit_placeholder"]},{100401})
  self.assertEqual(out["summary"]["same_original_SPR_number_index_sha_matches"],124)
  self.assertFalse(any(out["evidence_limits"].values()))
  self.assertEqual((out["private_viewer_reused_PNG_count"],out["private_viewer_reused_source_sequences"],out["private_viewer_reused_frame_occurrences"]),(2540,451,3817))
  self.assertFalse(out["private_asset_bytes_published_in_Git"])
  self.assertEqual(out["private_output_html_sha256"],"321d366313dc30d71fe1f3aa0bb7f9feb63e5a6c1e0aa5411b4975adf9f3afe9")
  self.assertEqual(out["current_state_preserved_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
  self.assertEqual(out["year_2000"],"OPEN_NOT_YEAR_CLOSED")
 def test_chronology_still_open(self):
  q=load("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
  self.assertEqual((q["current_frontier"]["year"],q["current_frontier"]["status"]),(2000,"OPEN_NOT_YEAR_CLOSED"))
  self.assertIn("PET46-TW1-ALBUM-PRIVATE-ORIGINAL-2D-20261116",[x["id"] for x in q["root_source_census_receipts"]])
  s=(ROOT/"docs/STONEAGE-PET-CHRONOLOGICAL-RESTORATION-ORDER-R1.md").read_text(encoding="utf-8")
  self.assertEqual(s.count("## PET46 2026-11-16"),1)
if __name__=="__main__":unittest.main()
