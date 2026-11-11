"""INTEGRATION69 derived source-conservation tests, never original gameplay execution.

Only numerical research, immutable file hashes and source-scoped negatives are public.
Original game files and PNGs must remain outside the GitHub repository.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'research/recovered'
TARGET=REC/'STONEAGE-INTEGRATION69-HEIRLOOM-EVENT13-NPC-ITEM-TW1-PIXEL-SOURCE-R1.json'
QUEST01=REC/'STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json'
CHAR01=REC/'STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
ITEM02=REC/'item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json'

SHA=lambda s:hashlib.sha256(s.encode('utf8')).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf8'))
def gitblob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def valid(r):
    assert r['schema']=='stoneage.integration69.heirloom_event13_two_original_npcs_five_original_item_candidates.r1'
    f=r['fresh_remote']; assert (f['historical_CURRENT_git_blob'],f['historical_CURRENT_bytes'],f['historical_CURRENT_edited'])==('c89e0e33537990aa2132b47c40fef49a985a935c',2709173,False)
    scope=r['source_scopes']
    assert 'MIXED25' in scope['NPC_create_quest_and_itemsets']
    assert 'AUTHENTIC_TW_WAEI_JSS_1_0' in scope['actual_RD_images']
    assert 'NOT_NATIVE_RUNTIME_LOOKUP' in scope['join_kind']
    assert (scope['legacy_QUEST01_scripts_already_catalogued'],scope['legacy_QUEST01_TYPE_sections_already_catalogued'])==(2,5)
    assert (scope['newly_discovered_original_quest_scripts'],scope['newly_discovered_TYPE_sections'],scope['newly_executed_native_game_events'])==(0,0,0)
    assert (scope['replayed_original_TW1_RD_blocks'],scope['original_NPC_RD_blocks_replayed'],scope['previously_saved_ITEM01_RDs_replayed_and_pixel_matched'])==(7,2,5)
    a=r['original_source_creates']; assert len(a)==2
    assert [(x['ordinal'],x['original_floor_id'],x['source_npc_graphic_alias'],x['linked_original_script']) for x in a]==[(0,1112,16000,'sainasu/event/event13_1'),(1,1100,16048,'sainasu/event/event13_2')]
    assert all(x['source_qualified_template_function']=='ExChangeMan' for x in a)
    assert [x['original_create_block_sha256'] for x in a]==['cd0d392d726239abb1be0355d6ccfc49d85e5e5bd29a6afc441e3b28d3838136','2ad0b6a1a5c29b384d041a05bdc3edf843f09f43f91ea06dc6d74d20a1d0dbc2']
    e=r['original_source_event_sections'];assert len(e)==5
    assert [x['source_type'] for x in e]==['ACCEPT','MESSAGE','REQUEST','MESSAGE','CLEAN']
    assert [x['source_event_no_literal'] for x in e]==['13','13','13','-1','-1']
    assert [x['source_type_line_1based'] for x in e]==[10,21,29,42,10]
    for x in e:
        assert SHA(x['source_condition_literal'])==x['source_condition_UTF8_sha256']
        assert x['source_action_execution_observed'] is False
        assert len(x['source_section_decoded_CP950_UTF8_sha256'])==64
        assert all(x['commands_in_physical_order'][i]['physical_line_1based']<x['commands_in_physical_order'][i+1]['physical_line_1based'] for i in range(len(x['commands_in_physical_order'])-1))
    static=r['original_static_relations']
    assert static['original_EVENT_ACCEPT_13_requires_exact_literal']=='NOWEV=13&ITEM=2428&ITEM=2429&ITEM=2430'
    assert static['original_EVENT_ACCEPT_13_DelItem_literal']=='2428,2429,2430,2431'
    assert static['original_EVENT_ACCEPT_13_GetItem_literal']=='2450'
    assert static['original_EVENT_ACCEPT_13_EndSetFlg_literal']=='13'
    assert static['original_EVENT_REQUEST_13_GetItem_literal']=='2431*1'
    assert static['original_young_NPC_CLEAN_13_condition_literal']=='ENDEV=13'
    assert static['original_young_NPC_CleanFlg_literal']=='13'
    assert static['the_event13_clean_rule_runtime_priority_or_replay_not_observed'] is True
    assert static['commands_are_static_source_tokens_not_actual_execution'] is True
    assert [[x['command'],x['original_value_literal']] for x in e[0]['commands_in_physical_order']]==[['GetItem','2450'],['DelItem','2428,2429,2430,2431'],['EndSetFlg','13']]
    assert [[x['command'],x['original_value_literal']] for x in e[-1]['commands_in_physical_order']]==[['CleanFlg','13']]
    it=r['original_two_table_item_source_rows']; assert len(it)==5
    assert [x['item_id'] for x in it]==[2428,2429,2430,2431,2450]
    assert [x['source_image_alias'] for x in it]==[21028,20018,21540,24222,24169]
    assert all(x['original_two_CP950_original_row_sha256']['itemset.txt']==x['original_two_CP950_original_row_sha256']['itemset0710.txt'] and x['source_original_94_fields']==94 for x in it)
    pix=r['source_qualified_TW1_retail_original_pixel_candidates']; assert len(pix)==7
    assert [x['source_graphic_alias'] for x in pix]==[16000,16048,21028,20018,21540,24222,24169]
    assert [x['actual_original_physical_bitmapno'] for x in pix]==[5846,5894,6329,5991,6405,6716,6995]
    assert all(x['unique_original_TW1_ADRN_alias_hits']==1 and x['source_pixel_decode_A_equals_independent_B'] is True for x in pix)
    assert all(x['original_source_retail_graphic_selector_executed'] is False for x in pix)
    assert all(x['previous_item01_original_RD_receipt_sha_match'] is True and x['previous_item01_PNG_RGBA_exact_match'] is True for x in pix[2:])
    assert all(x['naive_physical_bitmapno_equal_alias_is_wrong'] is True and x['naive_physical_bitmapno_ADRN_record_last_alias']!=x['source_graphic_alias'] for x in pix[:2])
    assert len({x['original_RD_sha256'] for x in pix})==7
    maps=r['source_map_qualifications'];assert [x['floor'] for x in maps]==[1112,1100]
    assert maps[0]['original_MAP09_source_ready_status']=='HAS_PRESERVED_SOURCE_READY_1112_DAT'
    assert maps[1]['original_MAP09_source_ready_status']=='NO_MATCHING_DAT_IN_955'
    assert maps[1]['does_NOT_prove_original_game_map_absent'] is True
    neg=r['copyright_and_historical_negative_bounds']
    assert all(value is False for value in neg.values())
    p=r['private_custody'];assert (p['zip_bytes'],p['private_zip_members'])==(75935,31)
    assert p['local_member_CRC_all_verified'] and p['personal_Library_uploaded_and_independently_reread']
    assert p['zip_sha256']=='054f01290d92f70fa36783c0273e99064d6e699a67fa098e7f141c70b893df47'
    status=r['project_status'];assert status['stage_A']=={'PARTIAL':7,'OPEN':2} and status['overall_percent'] is None
    assert status['stage_B']==status['wiki']=='GATED' and status['R79']=='PAUSED_NON_BLOCKING'
    return True

class Integration69(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=load(TARGET)
    def test_public_evidence_contract(self):self.assertTrue(valid(self.r))
    def test_reject_fake_early_official_deployment(self):
        x=copy.deepcopy(self.r);x['copyright_and_historical_negative_bounds']['same_early_official_server_deployment_across_sources_proven']=True
        with self.assertRaises(AssertionError):valid(x)
    def test_reject_fake_native_quest_run(self):
        x=copy.deepcopy(self.r);x['source_scopes']['newly_executed_native_game_events']=1
        with self.assertRaises(AssertionError):valid(x)
    def test_reject_missing_flag_13_CLEAN(self):
        x=copy.deepcopy(self.r);x['original_source_event_sections'].pop()
        with self.assertRaises(AssertionError):valid(x)
    def test_reject_mutated_delitem_original_order(self):
        x=copy.deepcopy(self.r);x['original_source_event_sections'][0]['commands_in_physical_order'][1]['original_value_literal']='2428,2429,2430'
        with self.assertRaises(AssertionError):valid(x)
    def test_reject_loss_of_two_different_source_NPCs(self):
        x=copy.deepcopy(self.r);x['original_source_creates'][1]['original_floor_id']=1112
        with self.assertRaises(AssertionError):valid(x)
    def test_reject_alias_as_physical_bitmap(self):
        x=copy.deepcopy(self.r);x['source_qualified_TW1_retail_original_pixel_candidates'][0]['actual_original_physical_bitmapno']=16000
        with self.assertRaises(AssertionError):valid(x)
    def test_reject_mutated_original_pixel_digest_count(self):
        x=copy.deepcopy(self.r);x['source_qualified_TW1_retail_original_pixel_candidates'][3]['original_RD_sha256']=x['source_qualified_TW1_retail_original_pixel_candidates'][2]['original_RD_sha256']
        with self.assertRaises(AssertionError):valid(x)
    def test_reject_five_prior_item_PNG_mismatch(self):
        x=copy.deepcopy(self.r);x['source_qualified_TW1_retail_original_pixel_candidates'][4]['previous_item01_PNG_RGBA_exact_match']=False
        with self.assertRaises(AssertionError):valid(x)
    def test_reject_fake_map_1100_absence(self):
        x=copy.deepcopy(self.r);x['source_map_qualifications'][1]['does_NOT_prove_original_game_map_absent']=False
        with self.assertRaises(AssertionError):valid(x)
    def test_reject_original_content_in_public(self):
        x=copy.deepcopy(self.r);x['copyright_and_historical_negative_bounds']['raw_original_TW1_RD_or_PNG_in_public_Git']=True
        with self.assertRaises(AssertionError):valid(x)
    def test_reject_current_history_replacement(self):
        x=copy.deepcopy(self.r);x['fresh_remote']['historical_CURRENT_edited']=True
        with self.assertRaises(AssertionError):valid(x)
    def test_reject_pretend_more_scripts_discovered(self):
        x=copy.deepcopy(self.r);x['source_scopes']['newly_discovered_original_quest_scripts']=1
        with self.assertRaises(AssertionError):valid(x)
    def test_reject_private_custody_without_reread(self):
        x=copy.deepcopy(self.r);x['private_custody']['personal_Library_uploaded_and_independently_reread']=False
        with self.assertRaises(AssertionError):valid(x)
    def test_existing_original_source_indices(self):
        """On full GitHub checkout, verify exact pre-existing Git source rather than trusting this report."""
        if not all(p.exists() for p in (QUEST01,CHAR01,ITEM02)):
            self.skipTest('Requires complete repository; run in exact GitHub Actions checkout')
        for p,sha in ((QUEST01,'52db8b4b6cd43cd2afa4a8d2e8460f214933f5e2'),(CHAR01,'a088b61a3212f7049e7793f587123ffb29bebad7'),(ITEM02,'b91bc8335db508998f4595144ce371979ea8c849')):
            self.assertEqual(gitblob(p.read_bytes()),sha)
        oldq=load(QUEST01);oldc=load(CHAR01);olditems=load(ITEM02)
        bypath={x['path']:x for x in oldq['source_scripts']}
        for old in self.r['source_files']['source_scripts']:
            x=bypath[old['source_path']]
            self.assertEqual((x['original_size'],x['original_sha256']), (old['raw_bytes'],old['source_full_CP950_sha256']))
        eventindex={(x['script_path'],x['script_block_ordinal']):x for x in oldq['source_event_blocks']}
        for e in self.r['original_source_event_sections']:
            old=eventindex[(e['script_path'],e['source_event_ordinal'])]
            self.assertEqual((e['source_type'],e['source_type_line_1based'],e['source_section_decoded_CP950_UTF8_sha256']), (old['raw_type'],old['source_type_line'],old['source_section_decoded_cp950_normalized_UTF8_sha256']))
            self.assertEqual(e['source_condition_UTF8_sha256'],old['condition_expression_decoded_cp950_UTF8_sha256'])
        bycreate={(x[0],x[1]):x for x in oldc['create_rows']}
        for x in self.r['original_source_creates']:
            old=bycreate[(x['original_create_file'],x['ordinal'])]
            self.assertEqual((old[4],old[5],old[6],old[7]), (x['original_create_block_sha256'],x['original_floor_id'],x['source_npc_graphic_alias'],x['borncorner_four_source_integers']))
            self.assertEqual(old[15][0][0],x['linked_original_script'])
        itemrows={x[0]:x for x in olditems['rows']}
        for x in self.r['original_two_table_item_source_rows']:
            o=itemrows[x['item_id']]
            self.assertEqual((o[1],o[2],o[3],o[4]),(x['original_two_CP950_original_row_sha256']['itemset.txt'],x['original_two_CP950_original_row_sha256']['itemset0710.txt'],x['source_image_alias'],x['source_image_alias']))

if __name__=='__main__':unittest.main()
