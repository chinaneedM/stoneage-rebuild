"""Only public evidence conservation. No private original commercial binaries required in CI."""
from __future__ import annotations
import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'research/recovered/STONEAGE-INTEGRATION119-TW10-16-SOURCE-QUALIFIED-2D-EFFECTLIKE-SPR-R1.json'
OLD11=ROOT/'research/recovered/STONEAGE-O11-NATIVE-FRAME-SOUND-SOURCE-R1.json'
OLD116=ROOT/'research/recovered/STONEAGE-INTEGRATION116-TEN-NPC-ORIGINAL-TW10-2D-R1.json'
OLD117=ROOT/'research/recovered/STONEAGE-INTEGRATION117-ORIGINAL-TW10-UNCLASSIFIED-TEN-SPR-ACTUAL-PIXELS-R1.json'
HEX=re.compile(r'^[0-9a-f]{64}$')
class SourceOriginalEffects(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.p=json.loads(PATH.read_text());cls.g=cls.p['source_groups'];cls.a=cls.p['actual_original_source_pixel_recovery'];cls.pr=cls.p['private_artifact']
 def test_01_existing_original_source_matches_prior_accepted_tw10(self):
  o=json.loads(OLD11.read_text());pins=o['source_pins'];x=self.p['original_retail_carrier']
  self.assertEqual(x['zip_sha256'],pins['tw1_p3h_archive_sha256'])
  for n,k in [('spr_1.bin','tw1_spr_sha256'),('spradrn_1.bin','tw1_spradrn_sha256')]:self.assertEqual(x['original_file_members_sha256'][n]['sha256'],pins[k])
  self.assertEqual(o['full_spr_inventory']['groups'],464)
  self.assertEqual(o['full_spr_inventory']['animations'],39065)
  self.assertEqual(o['full_spr_inventory']['frames'],242085)
 def test_02_exact_final_contiguous_spread_of_16_source_rows(self):
  self.assertEqual(self.a['actual_original_group_ids'],list(range(100600,100613))+[100650,100651,100652])
  self.assertEqual([x['original_graphic_number'] for x in self.g],self.a['actual_original_group_ids'])
  self.assertEqual([x['source_spradrn_index'] for x in self.g],list(range(448,464)))
  self.assertEqual(len(self.g),16)
 def test_03_actual_sequence_and_frame_reference_counts_not_distinct_images(self):
  self.assertEqual([self.a[k] for k in ('SPR_groups','sequences','original_ordered_frame_references','different_source_RD_bitmap_ids')],[16,28,524,230])
  self.assertEqual(sum(x['sequence_count'] for x in self.g),28)
  self.assertEqual(sum(x['frame_positions'] for x in self.g),524)
  self.assertEqual(sum(x['distinct_bitmap_references'] for x in self.g),230)
  self.assertGreater(524,230)
  self.assertEqual([x['sequence_count'] for x in self.g],[2]*12+[1]*4)
 def test_04_230_strict_original_RD_twice_and_real_hashes(self):
  self.assertEqual(self.a['strict_original_RD_canvas_double_decoded'],230)
  self.assertEqual(self.a['bounded_terminal_zero_canvas_exception'],0)
  self.assertEqual(self.a['source_original_RD_flag_1'],230)
  self.assertEqual(self.a['source_original_RD_flag_0'],0)
  self.assertEqual(self.a['source_decoded_index_pixels'],1195780)
  self.assertEqual(self.a['different_source_bitmap_IDs_min_max'],[7004,7245])
  for k in ['source_original_RD_per_bitmap_SHA256_aggregate','source_original_decoded_index_pixels_per_bitmap_SHA256_aggregate']:self.assertRegex(self.a[k],HEX)
 def test_05_source_sha_and_raw_order_preserved_no_native_duration(self):
  self.assertEqual([x['direction_codes'] for x in self.g],[[0]]*16)
  self.assertEqual(sum(x['nonzero_frame_word_occurrences'] for x in self.g),0)
  self.assertEqual([x['action_codes'] for x in self.g],[[0,1]]*12+[[0]]*4)
  for x in self.g:
   self.assertRegex(x['original_SPRADRN_row_SHA256'],HEX)
   self.assertRegex(x['original_SPR_segment_SHA256'],HEX)
   self.assertEqual(len(x['source_spr_sequence_hashes']),x['sequence_count'])
   self.assertTrue(all(HEX.fullmatch(s) for s in x['source_spr_sequence_hashes']))
   self.assertTrue(x['original_SPR_segment_bytes']>0)
   self.assertTrue(all(type(d)==int and d>0 for d in x['raw_duration_values']))
  self.assertFalse(self.a['native_animation_timing_from_duration_raw_proven'])
  self.assertFalse(self.a['native_sound_word_playback_proven'])
 def test_06_prior_group_identity_no_duplicates_vs_previous_two_packages(self):
  ids=set(self.a['actual_original_group_ids'])
  p=json.loads(OLD116.read_text());q=json.loads(OLD117.read_text())
  self.assertFalse(ids.intersection(x['graphic'] for x in p['source_groups']))
  self.assertFalse(ids.intersection(x['graphic'] for x in q['groups']))
  self.assertFalse(self.a['count_new_vs_all_prior_historical_bitmap_work_claimed'])
 def test_07_private_art_not_smisrepresented_as_source_native_client(self):
  self.assertEqual(self.pr['members'],235)
  self.assertEqual(self.pr['source_derived_grayscale_PNG_count'],230)
  self.assertEqual(self.pr['size_bytes'],190102)
  self.assertEqual(self.pr['sha256'],'530ff02f68a1511873cee5ddf479c55a04e4291ccdac90a5518fdb790ac48c32')
  self.assertTrue(self.pr['contains_true_proprietary_sprite_art_private_only'])
  self.assertFalse(self.pr['source_RD_or_SPR_original_raw_binaries_in_package'])
  self.assertFalse(self.pr['HTML_file_scheme_browser_tested'])
  for k in ('native_client_executed','historical_palette_and_native_compositing_verified','native_effect_name_or_trigger_proven','crosscarrier_later_item_name_or_effect_identity_verified','no_original_source_RD_SPR_binaries_in_public_Git'):
   self.assertEqual(self.a[k],k=='no_original_source_RD_SPR_binaries_in_public_Git')
 def test_08_historical_limits_and_raw_proprietary_leak_negative(self):
  self.assertEqual(self.p['historical_CURRENT_blob_unchanged'],'c89e0e33537990aa2132b47c40fef49a985a935c')
  self.assertEqual(self.p['project_state']['StageA'],'7 PARTIAL + 2 OPEN')
  self.assertEqual(self.p['project_state']['StageBWiki'],'GATED')
  self.assertIsNone(self.p['project_state']['overall_percent'])
  self.assertTrue(self.p['source_only_not_native_gameplay'])
  self.assertNotIn('real_original_RD_binary_base64',self.p)
  self.assertNotIn('actual_PNG_bytes',self.p)
  self.assertFalse(any('original_raw_bitmap_pixels' in x for x in self.g))
if __name__=='__main__':unittest.main()
