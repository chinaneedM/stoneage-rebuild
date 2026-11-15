"""Source-bound derived audit only. Private commercial original SPR/RD are NOT in CI."""
from __future__ import annotations
import json
from pathlib import Path
from copy import deepcopy
import unittest

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-INTEGRATION115-TW10-FIVE-GATE-BREEDER-ACTUAL-ORIGINAL-2D-R1.json'
PARENT=ROOT/'research/recovered/STONEAGE-INTEGRATION114-GATE-BREEDER-ORIGINAL-SOURCE-R1.json'
EXPECTED={
 100431:(394,592,'3adc4cbb86bd45145ae0fa15004d5e7183bd208fb3bfc686c84ce13b711a4c9e',87631),
 100439:(402,488,'456e1890d6c77d0a4b6edd0fa9ce3a5a72968bbcedca5a653b707fef594139e2',89503),
 100436:(399,592,'d582ab127e7a0626adca1bf1c7c7dce0c21ae7ed24c184ea5f4f40ca7157b49e',89159),
 100407:(370,352,'4943ed6023ab83b3ecc6b923906d068a0083a3190a63b7075cb85012fb2d6a18',84847),
 100437:(400,472,'0a5156c00d2c348164400cf849a2165cfd3d4e3f061cb24e5dcc4b873693faab',88271),
}
ZIP_SHA='3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24'

def verify(r,parent):
 assert r['schema']=='stoneage.integration115_tw10_original_five_npc_graphic_2d_source_candidates.r1'
 src=r['source_original'];later=r['separate_later_game_source'];o=r['actual_source_observation'];neg=r['negative_evidence_limits']
 assert src['carrier']=='AUTHENTICATED_TW_WAEI_JSS_1_0_RETAIL_REDUMP_104630_NOT_JSS1999'
 assert src['private_zip_bytes']==372626292 and src['private_zip_sha256']==ZIP_SHA
 assert src['verified_zip_member_crc_count']==379
 assert (src['TW1_original_total_SPRADRN_groups'],src['TW1_original_total_ADRN_bitmap_rows'])==(464,125996)
 assert src['authenticated_original_source_members']['real_1.bin']=={'bytes':315842228,'sha256':'408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13'}
 assert src['authenticated_original_source_members']['spradrn_1.bin']['bytes']==5568
 assert later['carrier'].startswith('LATER_PRESERVED_COMMUNITY')
 assert later['reference'].endswith('STONEAGE-INTEGRATION114-GATE-BREEDER-ORIGINAL-SOURCE-R1.json')
 assert later['five_source_CREATE_graphic_ids']==list(EXPECTED)
 assert (later['JBA_CREATE_graphicname'],later['JBA_template_type'],later['must_preserve_type_mismatch'])==(100437,100436,True)
 assert sorted(x['original_graphicname'] for x in parent['original_source_rows'])==sorted(EXPECTED)
 assert any(x['original_graphicname']==100437 and x['original_template_type']==100436 for x in parent['original_source_rows'])
 groups=r['five_groups'];assert len(groups)==5 and [x['graphic_no'] for x in groups]==list(EXPECTED)
 assert len(set(x['source_SPRADRN_index'] for x in groups))==5
 for row in groups:
  gid=row['graphic_no'];idx,frames,sha,first=EXPECTED[gid]
  assert (row['source_SPRADRN_index'],row['original_frame_positions'],row['original_SPR_segment_sha256'])==(idx,frames,sha)
  assert (row['original_animation_sequences'],row['original_direction_count'])==(104,8)
  assert row['original_action_codes']==list(range(13))
  assert row['distinct_original_bitmap_ids']==344
  assert row['original_RD_blocks_read_and_independently_decoded']==344
  assert row['first_action0_direction0_original_bitmap_no']==first
  assert row['source_zero_sentinel_frames']==0 and row['distinct_group_bitmap_record_count_matches'] is True
  assert row['candidate_color_and_source_native_render_proven'] is False
  for name in ('original_SPRADRN_record_sha256','all_original_RD_sha256_sequence_sha256','decoded_original_source_bitmap_index_sha256_sequence_sha256','sample_frame_original_RD_sha256'):
   assert isinstance(row[name],str) and len(row[name])==64
 assert sum(x['original_frame_positions'] for x in groups)==2496
 assert sum(x['distinct_original_bitmap_ids'] for x in groups)==1720
 assert o['five_unique_original_SPR_index_rows']==5
 assert o['distinct_source_RD_bitmap_blocks_directly_reread_and_decoded']==o['source_RD_records_w_two_independent_pixel_decoder_agreement']==o['distinct_cross_group_bitmaps']==o['direct_source_RD_strict_count']==1624
 assert o['groups_reference_total_distinct']==1720
 assert o['direct_source_RD_bounded_anomaly_count']==0 and o['RD_flag_one_count']==1624 and o['RD_flag_zero_count']==0
 assert o['sum_decoded_visible_index_pixels_across_distinct_RD']==6104074
 assert o['all_exact_original_RD_SHA256_sequence_sha256']=='9b6bc1ec578308b71cc1673716db6cedd331940c53d08e1c6219480e9ce417df'
 assert o['all_exact_decoded_index_pixels_sha256_sequence_sha256']=='ea7f6860fe7b028f33c09ea6c27e4f2ebd9da329a81a2837a96306298449c5b7'
 assert o['original_tw1_bitmaps_generated_privately_as_candidate_palette_0_and_1_contact_sheets'] is True
 assert o['private_contact_sheets_only_not_public']==2
 for key in ('new_independent_original_client_acquired','same_historical_TW1_and_mixed25_deployment_proven','native_game_sprite_graphicname_vs_template_type_selection_proven','native_game_played','original_server_npc_spawn_or_enemy_execution_proven','actual_original_scene_palette_selection_proven','private_proprietary_RD_or_SPR_or_PNG_published','historical_pet_or_npc_identities_derived_from_same_numeric_ID'):
  assert neg[key] is False,key
 assert neg['stage_a']=='7_PARTIAL_2_OPEN' and neg['stage_b_wiki']=='GATED' and neg['r79']=='PAUSED_NON_BLOCKING' and neg['overall_percent'] is None
 return True

class TestOriginalTrue2D(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.report=json.loads(REPORT.read_text(encoding='utf-8'))
  cls.parent=json.loads(PARENT.read_text(encoding='utf-8'))
 def test_original_derived_cross_reference(self): self.assertTrue(verify(self.report,self.parent))
 def test_jba_numeric_disagreement_must_survive(self):
  r=deepcopy(self.report);r['separate_later_game_source']['JBA_template_type']=100437
  with self.assertRaises(AssertionError):verify(r,self.parent)
 def test_no_invented_native_execution(self):
  r=deepcopy(self.report);r['negative_evidence_limits']['native_game_played']=True
  with self.assertRaises(AssertionError):verify(r,self.parent)
 def test_no_invented_same_deployment(self):
  r=deepcopy(self.report);r['negative_evidence_limits']['same_historical_TW1_and_mixed25_deployment_proven']=True
  with self.assertRaises(AssertionError):verify(r,self.parent)
 def test_reject_wrong_rd_count(self):
  r=deepcopy(self.report);r['actual_source_observation']['direct_source_RD_strict_count']=1623
  with self.assertRaises(AssertionError):verify(r,self.parent)
 def test_reject_wrong_original_segment(self):
  r=deepcopy(self.report);r['five_groups'][0]['original_SPR_segment_sha256']='0'*64
  with self.assertRaises(AssertionError):verify(r,self.parent)
 def test_reject_wrong_frame_count(self):
  r=deepcopy(self.report);r['five_groups'][0]['original_frame_positions']+=1
  with self.assertRaises(AssertionError):verify(r,self.parent)
 def test_reject_wrong_original_source_carrier(self):
  r=deepcopy(self.report);r['source_original']['carrier']='OFFICIAL_JSS1999'
  with self.assertRaises(AssertionError):verify(r,self.parent)
 def test_reject_private_asset_publication(self):
  r=deepcopy(self.report);r['negative_evidence_limits']['private_proprietary_RD_or_SPR_or_PNG_published']=True
  with self.assertRaises(AssertionError):verify(r,self.parent)
 def test_reject_false_original_palette_certainty(self):
  r=deepcopy(self.report);r['negative_evidence_limits']['actual_original_scene_palette_selection_proven']=True
  with self.assertRaises(AssertionError):verify(r,self.parent)

if __name__=='__main__': unittest.main()