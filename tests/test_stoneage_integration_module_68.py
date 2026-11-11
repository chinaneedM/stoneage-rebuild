"""INTEGRATION68 public source/negative-boundary replay (no proprietary assets)."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'research/recovered'
REPORT=REC/'STONEAGE-INTEGRATION68-FOUR-VILLAGE-QUEST-NPC-FOUR-TW1-ORIGINAL-PIXELS-R1.json'
QUEST31=REC/'STONEAGE-QUEST31-FOUR-VILLAGE-EVENT09-12-SOURCE-R1.json'
SHA='[a-f0-9]{64}'

def read_json(path):
    return json.loads(path.read_text(encoding='utf8'))

def git_blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def audit(report, previous):
    assert report['schema']=='stoneage.integration68.quest31_four_npc_tw1_original_pixel_crosscarrier_candidates.r1'
    assert report['public_upstream_QUEST31_original_source_git_blob']==git_blob(QUEST31.read_bytes())=='0a17857fc55fd5884963d1c00ffeb292ebc9f59b'
    assert report['preserved_original_CURRENT_git_blob']==previous['initial_remote']['preserved_CURRENT_git_blob']=='c89e0e33537990aa2132b47c40fef49a985a935c'
    assert report['preserved_original_CURRENT_bytes']==2709173
    pins=report['provenance']
    assert pins['mixed25_quest31_original_private_zip_sha256']=='796682fd3621a2bfecab03e7e199ca16936f95cad75f6a7842e6517f1e04dd42'
    assert pins['original_mixed25_CREATE_sha256']==previous['original_files'][0]['sha256']=='1f55bbd59aa01c3aeaf1a70d5eb7b29f6c77f0dfd3549f082419c6e465a107e5'
    assert pins['original_mixed25_CREATE_bytes']==692
    assert pins['original_tw1_clean_retail_P3H_zip_sha256']=='3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24'
    assert (pins['original_tw1_ADRN_bytes'],pins['original_tw1_ADRN_sha256'])==(10079680,'47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8')
    assert (pins['original_tw1_REAL_bytes'],pins['original_tw1_REAL_sha256'])==(315842228,'408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13')
    assert (pins['original_tw1_Palet_1_SAP_bytes'],pins['original_tw1_Palet_1_SAP_sha256'])==(708,'32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0')
    p=report['actual_private_source_observation']
    assert p['original_P3H_and_QUEST31_ZIP_sha256_verified'] is True
    assert p['original_ADRN_REAL_Palet_bytes_sha256_verified'] is True
    assert p['original_mixed25_CREATE_sha256_verified'] is True
    assert p['original_tw1_ADRN_full_125996_records_scan'] is True
    assert (p['selected_original_source_RD_blocks_redecoded'],p['two_independent_RD_decoder_exact_index_pixel_matches'],p['four_original_private_PNG_candidates_rendered'])==(4,4,4)
    assert (p['new_original_NPC_source_script_count'],p['new_original_quest_TYPE_count'])==(0,0)
    rows=report['source_records']
    assert len(rows)==4
    assert [r['original_mixed25_graphic_alias'] for r in rows]==[16205,16206,16203,16057]
    assert [r['cross_carrier_tw1_actual_physical_bitmapno'] for r in rows]==[5925,5926,5923,5903]
    assert [(r['original_tw1_RD_width'],r['original_tw1_RD_height']) for r in rows]==[(40,93),(36,94),(32,87),(36,66)]
    assert [r['original_tw1_RD_block_sha256'] for r in rows]==[
      '86afdef71624ab1737640ff76da6b9d792a8970ff41468d095542980bfd5ac02',
      '6574c56633ddd50db2195a58d29a4aa7df470eef049b619d2d33ded2377e55f5',
      '1cec8ad8363001806d638fea3d6896636910ffdf7fd1a3d4686b829bcdff1454',
      'efe3520d7c981978a68904f0a45d8420bda2d3a01f10688661ce4b85e33c8603']
    assert [r['original_tw1_RD_index_pixels_sha256'] for r in rows]==[
      'dc6016cdba5843aa6f72293e834b9ce3ba760636e44af9144a48fea9921dc964',
      'e30b72fab0fac923f12c6618a0aeca24fc20076256457d4c5a361b52c9ee07be',
      '445b54b377514d7a297bab268bb319120da639ca069225628f2c6d92a212f439',
      '2c05f3a8da2a6217cc1a50c33d76831f9ce527c0c5478252e7dfd3558b9fb1d4']
    assert [r['private_original_tw1_Palet1_candidate_PNG_sha256'] for r in rows]==[
      '8b674cecc59fc4eb41ab0d36ffef60b8346e1d082e45b8ec0018f6851d0cbec5',
      '7c66c876dfafb81cf42f6288cbc67a6ba755dd2c5a986c6b60084c14cf068d22',
      '42dcc425b36d02445d3843758e503b5d03264b1e7638c5cf5bd1ca0abc942fa5',
      'ba262bf3e02c23368929a9f10c4c13fc20f29fcbf685889408a6159e3ac5d17e']
    for row,old in zip(rows,previous['source_create_records']):
        assert row['source_quest31_create_ordinal']==old['ordinal']
        assert row['original_mixed25_source_create_path']==old['create_path']
        assert row['original_mixed25_source_create_block_sha256']==old['source_block_sha256']
        assert row['original_mixed25_floor']==old['floor']
        assert row['original_mixed25_birth_corner_four_numbers']==old['borncorner_original_four_numbers']
        assert row['original_mixed25_direction_raw']==old['direction']
        assert row['original_mixed25_graphic_alias']==old['graphic_alias']
        assert row['original_mixed25_script_path']==old['script_path']
        assert row['original_mixed25_map_source_status']==old['map_source_status']
        assert row['cross_carrier_tw1_unique_ADRN_alias_count']==1
        assert row['cross_carrier_tw1_original_ADRN_record_index']==row['cross_carrier_tw1_actual_physical_bitmapno']
        assert row['original_tw1_RD_flag']==1
        assert row['original_tw1_source_index_values_outside_16_to_239_except_zero']=={}
        assert row['same_official_deployment_or_original_NPC_native_draw_proven'] is False
        assert row['wrong_namespace_physical_bitmapno_equal_to_source_graphic_alias']['physical_bitmapno']==old['graphic_alias']
        assert row['wrong_namespace_physical_bitmapno_equal_to_source_graphic_alias']['tw1_ADRN_record_alias_at_plus_76']==0
        assert row['wrong_namespace_physical_bitmapno_equal_to_source_graphic_alias']['same_pixels_as_alias_qualified_bitmap'] is False
        for key in ('original_tw1_ADRN_80_byte_sha256','original_tw1_RD_block_sha256','original_tw1_RD_index_pixels_sha256','private_original_tw1_Palet1_candidate_RGBA_sha256','private_original_tw1_Palet1_candidate_PNG_sha256'):
            assert re.fullmatch(SHA,row[key]),(key,row[key])
    assert report['counts']=={'mixed25_original_NPC_CREATE_records':4,'unique_original_tw1_ADRN_aliases':4,'unique_original_tw1_physical_bitmaps':4,'unique_original_tw1_RD_index_pixel_shas':4,'source_qualified_orig_DAT_floors_from_prior_QUEST31':3,'original_DAT_floor_1300_missing_in_prior_955_ready_batch':True}
    custody=report['private_custody']
    assert (custody['zip_bytes'],custody['zip_members'],custody['zip_sha256'])==(24425,11,'e3b18f6b43d749bdda3fbbdf20e745e1c9c0da338c4d4cd446dbd4f4263ed0c0')
    assert custody['local_all_ZIP_member_CRC_and_exact_bytes_verified'] is True
    assert custody['library_uploaded_and_reread'] is True
    assert custody['independent_library_download_zip_bytes_same_sha_crc_all_members'] is True
    assert custody['library_path'].startswith('/石器时代/StoneAge-INTEGRATION68-')
    b=report['bounded_negative_claims']
    assert all(value is False for value in b.values())
    assert len(b)==8
    assert report['stage_A']=={'PARTIAL':7,'OPEN':2}
    assert report['stage_B']=='GATED' and report['wiki']=='GATED' and report['R79']=='PAUSED_NON_BLOCKING'
    assert report['overall_percent'] is None
    return True

class Integration68(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=read_json(REPORT);cls.q=read_json(QUEST31)
    def test_exact_public_source_join_and_custody(self):
        self.assertTrue(audit(self.r,self.q))
    def test_reject_false_official_same_build_claim(self):
        r=copy.deepcopy(self.r);r['bounded_negative_claims']['later_community_mixed25_and_earlier_authentic_tw1_original_same_official_deployment']=True
        with self.assertRaises(AssertionError):audit(r,self.q)
    def test_reject_wrong_create_alias(self):
        r=copy.deepcopy(self.r);r['source_records'][1]['original_mixed25_graphic_alias']=16203
        with self.assertRaises(AssertionError):audit(r,self.q)
    def test_reject_physical_alias_namespace_swap(self):
        r=copy.deepcopy(self.r);r['source_records'][0]['cross_carrier_tw1_actual_physical_bitmapno']=16205
        with self.assertRaises(AssertionError):audit(r,self.q)
    def test_reject_false_source_reread_crc(self):
        r=copy.deepcopy(self.r);r['private_custody']['independent_library_download_zip_bytes_same_sha_crc_all_members']=False
        with self.assertRaises(AssertionError):audit(r,self.q)
    def test_reject_wrong_source_rd_sha(self):
        r=copy.deepcopy(self.r);r['source_records'][3]['original_tw1_RD_block_sha256']='0'*64
        with self.assertRaises(AssertionError):audit(r,self.q)
    def test_reject_wrong_original_png_sha(self):
        r=copy.deepcopy(self.r);r['source_records'][2]['private_original_tw1_Palet1_candidate_PNG_sha256']='0'*64
        with self.assertRaises(AssertionError):audit(r,self.q)
    def test_reject_false_1300_map_recovery(self):
        r=copy.deepcopy(self.r);r['bounded_negative_claims']['original_floor_1300_DAT_or_scene_recovered']=True
        with self.assertRaises(AssertionError):audit(r,self.q)
    def test_reject_fabricated_native_gameplay(self):
        r=copy.deepcopy(self.r);r['bounded_negative_claims']['original_quest_execution_or_NPC_dialogue_replayed']=True
        with self.assertRaises(AssertionError):audit(r,self.q)
    def test_reject_legacy_source_mutation(self):
        r=copy.deepcopy(self.r);q=copy.deepcopy(self.q)
        q['source_create_records'][0]['source_block_sha256']='0'*64
        with self.assertRaises(AssertionError):audit(r,q)

if __name__=='__main__':unittest.main()
