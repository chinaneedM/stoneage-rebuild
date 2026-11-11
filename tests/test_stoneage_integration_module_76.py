"""Integration76: source-bound anniversary cake static evidence, never active-world proof."""
import copy, hashlib, json, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
DERIVED=ROOT/'research/recovered/STONEAGE-INTEGRATION76-ANNIVERSARY-CAKE-ORIGINAL-IMAGE-SOURCE-R1.json'
SHARD=ROOT/'research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-05-R1.json'
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def validate(r):
 assert r['schema']=='stoneage.integration76.anniversary_cake_source_and_TW1_original_pixel_candidate.r1'
 assert r['restart']['historical_CURRENT_blob']=='c89e0e33537990aa2132b47c40fef49a985a935c'
 assert r['restart']['historical_CURRENT_bytes']==2709173
 n=r['existing_original_NPC_carrier'];s=n['original_event_script'];c=n['original_NPC_CREATE_file']
 assert n['SHA256']=='c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f'
 assert n['total_member_count']==2205 and n['all_ZIP_CRC_verified']
 assert (s['bytes'],s['original_event_blocks'],s['source_ordered_TYPES'])==(576,2,['ACCEPT','MESSAGE'])
 assert (s['source_ACCEPT_item_not_equal'],s['source_ACCEPT_GetItem'],s['source_MESSAGE_item_equals'])==(13030,13030,13030)
 assert s['SHA256']=='a82020cdbf3fa2999b1f784025220aacc39910a012ba07c6f1aa5e00a18f9f35'
 assert c['bytes']==633 and c['SHA256']=='b9c6e9a8d3a8fb3f8848853f1460d365166b58fe2460537574a49a0110db49f3'
 assert c['all_nonblank_lines_begin_with_comment_marker'] and c['original_commented_NPC_CREATE_blocks']==4
 assert c['active_uncommented_CREATE_blocks']==0
 assert c['original_commented_graphicname']==41000 and c['original_commented_enemy_pointer']=='extra/event/cake'
 assert [(x['floorid'],x['corner']) for x in c['source_commented_create_positions']]==[(1000,[92,87,92,87]),(2000,[59,74,59,74]),(3000,[76,104,76,104]),(4000,[72,76,72,76])]
 scan=n['bounded_direct_reference_scan']
 assert scan['scanned_NPC_ZIP_members']==2205
 assert scan['matching_paths']==['npc/extra/event/cake.create'] and scan['direct_uncommented_matching_CREATE_references']==0
 a=r['old_ITEM01_original_source_verified_transcriptions']
 assert a['original_parent_itemset_RAR_members_reread_this_unit'] is False
 assert (a['ZIP_member_count'],a['all_ZIP_CRC_verified'])==(838,True)
 assert a['original_item_ID']==13030
 assert (a['original_itemset_txt_row_1based'],a['original_itemset0710_txt_row_1based'])==(7680,8131)
 assert a['original_itemset_txt_complete_row_SHA256']==a['original_itemset0710_txt_complete_row_SHA256']=='56862b87ecc2873a4addf7cd4078d57edfb7f59fcfaed4b986365079d28627f8'
 assert (a['raw_original_image_alias_A'],a['raw_original_image_alias_B'])==(24409,24409)
 assert a['retail_TW1_original_RD_evidence_class']=='REAL_RD_DECODED_CROSS_CARRIER'
 p=r['old_separately_verified_TW1_retained_original_pixel']
 assert (p['physical_original_ADRN_ordinal'],p['physical_original_bitmap_number'])==(6576,6576)
 assert (p['original_width'],p['original_height'],p['original_RD_bytes'])==(56,36,1341)
 assert p['original_RD_SHA256']=='6049d5fb44bec2e3af58401724bfc457648ac810ac31d959d6e28d025bf0d556'
 assert p['retained_candidate_PNG_SHA256']=='9ac9c3fa1801e0345ea2f9c157900c2f8a25a5b587272ff01a35e3df04cd621b'
 assert p['retained_candidate_RGBA_SHA256']=='0f040499540912f5dd394cf3fc884dd2fa69118b06f2aeac595f504979285f9b'
 assert p['new_original_RD_decodes_this_unit']==0
 assert p['old_original_RD_SHA256_qualified_from_ITEM01_not_independently_redecoded_this_unit']
 assert p['non_identical_NPC_graphic_alias_41000_and_item_image_alias_24409']
 custody=r['private_independent_custody']
 assert (custody['bytes'],custody['member_count'])==(7317,7)
 assert custody['ZIP_SHA256']=='ae3299cd3af4502feced37052a9ae290a18875f10ecef86ceab5c49a027784fd'
 assert custody['all_member_CRC_verified_on_independent_library_readback'] and custody['downloaded_Library_byte_for_byte_match']
 assert custody['public_Git_original_bytes_added']==0
 assert not any(r['not_proven'].values())
 assert (r['status']['stage_A_PARTIAL'],r['status']['stage_A_OPEN'])==(7,2) and r['status']['overall_percent'] is None
 return True
class TestCakeProvenance(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=load(DERIVED);cls.shard=load(SHARD)
 def test_source_contracts(self):self.assertTrue(validate(self.r))
 def test_old_item01_original_94column_row_and_source_alias(self):
  s=self.shard;r=self.r['old_ITEM01_original_source_verified_transcriptions']
  self.assertEqual(s['source_itemset_rows_sha256_provenance'],'a415e78f9aab2e5ea5ca92ecb7430253f7be1ba7c876d6b0bb6d067b1b466688')
  self.assertEqual(s['source_itemset0710_rows_sha256_provenance'],'6d6d63fda59c6bda2f239fe18c9361b5c9da18c84f678b7cc95bde24544292fb')
  row=next(x for x in s['rows'] if x[0]==13030)
  self.assertEqual(row[1:5],[r['original_itemset_txt_complete_row_SHA256'],r['original_itemset0710_txt_complete_row_SHA256'],24409,24409])
  self.assertEqual(row[8:11],['REAL_RD_DECODED_CROSS_CARRIER','REAL_RD_DECODED_CROSS_CARRIER',[]])
 def reject(self,fn):
  x=copy.deepcopy(self.r);fn(x)
  with self.assertRaises(AssertionError):validate(x)
 def test_negative_false_active_NPC(self):self.reject(lambda x:x['existing_original_NPC_carrier']['original_NPC_CREATE_file'].update(active_uncommented_CREATE_blocks=4))
 def test_negative_erase_comment_state(self):self.reject(lambda x:x['existing_original_NPC_carrier']['original_NPC_CREATE_file'].update(all_nonblank_lines_begin_with_comment_marker=False))
 def test_negative_wrong_real_icon(self):self.reject(lambda x:x['old_ITEM01_original_source_verified_transcriptions'].update(raw_original_image_alias_B=41000))
 def test_negative_native_event_activated(self):self.reject(lambda x:x['not_proven'].update(anniversary_event_deployment=True))
 def test_negative_claim_new_RD(self):self.reject(lambda x:x['old_separately_verified_TW1_retained_original_pixel'].update(new_original_RD_decodes_this_unit=1))
 def test_negative_original_year_assertion(self):self.reject(lambda x:x['not_proven'].update(first_edition_or_1999_origin=True))
 def test_negative_publish_copyrighted_source(self):self.reject(lambda x:x['private_independent_custody'].update(public_Git_original_bytes_added=2))
if __name__=="__main__":unittest.main()
