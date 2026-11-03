"""Public QUEST04 source qualification, numeric consistency & negative-evidence guards."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]/'research'/'recovered'
INDEX=ROOT/'STONEAGE-QUEST04-SOURCE-BOUNDED-FAMILIES-R1.json'
CHAR=ROOT/'STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
ITEMS=[ROOT/'item-module-01'/f'STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{i:02d}-R1.json' for i in range(1,8)]
HEX=re.compile(r'^[a-f0-9]{64}$')

def verify(d, char, itemshards):
    assert d['schema']=='stoneage.quest_story_module04_source_bounded_family_completion.r1'
    assert d['source']['original_parent_RAR_not_reread_this_turn'] is True
    assert HEX.fullmatch(d['source']['private_ZIP_sha256_current_replay'])
    assert (d['source']['source_original_npc_files_SHA_CRC_replayed'],d['source']['source_original_npc_bytes_SHA_CRC_replayed'])==(2205,1930332)
    creates=d['source_create_references']; files=d['source_parameter_files']; s=d['summary']
    assert len(creates)==len(files)==s['reviewed_create_references']==s['actual_source_parameter_files']==25
    manifest={x[0]:x for x in char['source_files']}; rows={(r[0],r[1]):r for r in char['create_rows']}
    bypath={}
    for f in files:
        p=f['path']; assert p not in bypath and p in manifest
        m=manifest[p]; assert (f['original_size_bytes'],f['original_sha256'],f['original_crc32'])==(m[1],m[2],m[3])
        assert HEX.fullmatch(f['original_sha256']) and re.fullmatch(r'[a-f0-9]{8}',f['original_crc32'])
        assert f['origin_class']=='ORIGIN_UNRESOLVED' and f['native_server_execution_observed'] is False
        bypath[p]=f
    counts=Counter(); fc=Counter()
    for c in creates:
        r=rows[(c['create_source_path'],c['create_source_block_ordinal'])]
        assert r[4]==c['source_create_block_sha256'] and HEX.fullmatch(c['source_create_block_sha256'])
        assert r[5]==c['floorid_numeric'] and r[6]==c['graphic_numeric'] and r[11]==c['function_token']
        assert r[15]==[[c['source_param_path'],'EXACT_SAME_NPC_SUBTREE_PATH',c['source_param_sha256']]]
        assert c['source_param_sha256']==bypath[c['source_param_path']]['original_sha256']
        counts[c['source_param_path']]+=1;fc[c['function_token']]+=1
    assert all(f['create_references']==counts[f['path']] for f in files)
    assert s['family_create_counts']==dict(sorted(fc.items()))
    assert fc['npcgen_janken']==9 and fc['npcgen_action']==8 and fc['npc_raceman']==1
    assert sum(v for k,v in fc.items() if k.startswith('event69_'))==7
    assert len(fc)==10
    assert s['QUEST01_create_ref_count']+s['QUEST02_create_ref_count']+s['QUEST03_create_ref_count']+s['QUEST04_create_ref_count']+s['remaining_other_function_create_refs_not_assumed_quest']==4985
    assert len({r[11] for r in char['create_rows']})==s['full_4985_CREATE_functionset_tokens']==91
    quiz_floors={r[5] for r in char['create_rows'] if r[11]=='npcgen_quiz'}
    jk=[f for f in files if f['template_family']=='npcgen_janken']
    for f in jk:
        c=next(c for c in creates if c['source_param_path']==f['path'])
        assert (f['entry_item_id'],f['entry_item_qty'])==(2751,1)
        assert len(f['winwarp_literal'])==len(f['losewarp_literal'])==3
        assert f['winwarp_literal'][0]==c['floorid_numeric']
        assert f['losewarp_literal'][0] in quiz_floors
    assert s['janken_winwarp_9_of_9_points_to_same_source_floor'] is True
    assert s['janken_losewarp_9_of_9_target_QUIZ03_create_source_floor'] is True
    actions=[f for f in files if f['template_family']=='npcgen_action']
    expected=['normal','attack','damage','down','sit','hand','pleasure','angry','sad','guard','nod','throw']
    assert all(f['action_message_key_names']==expected and f['source_action_message_slot_count']==12 for f in actions)
    ev=[f for f in files if f['template_family'].startswith('event69_')]
    assert sum(f['numbered_NEWEVENT_segments'] for f in ev)==s['event69_raw_NEWEVENT_sections']==3
    assert all(len(f['warp_literal'])==3 and len(f['enemy_instance_numbers'])>0 for f in ev)
    race=next(f for f in files if f['template_family']=='npc_raceman')
    assert race['source_text_date_ymd']=='2004-12-22'
    assert (race['source_CheckItem'],race['source_GetItem'],race['source_HasGame_numeric'],race['source_GameMode_numeric'])==(20760,20760,5,5)
    assert race['source_deployment_authentication']=='UNVERIFIED'
    article=d['independently_reported_2004_operator_event']
    assert article['published']=='2004-12-11' and article['claimed_start']=='2004-12-08'
    assert article['claimed_end']=='2004-12-22 08:00 (reported local)'
    assert article['event_historical_origin']=='OPERATOR_EVENT_QUEST'
    assert article['source_url']=='https://www.games.idv.tw/news.php?nid=236'
    assert sum(1 for f in files if f['template_family']=='npc_raceman' and f['historical_reported_operator_event_crosssource_candidate'])==1
    itemmap={}
    for sh in itemshards:
        for row in sh['rows']:
            if row[0] in (1292,2751,2752,2753,19622,20760):itemmap[row[0]]={'item_table_A':row[1] is not None,'item_table_B':row[2] is not None}
    assert {str(k):v for k,v in sorted(itemmap.items())}==s['item_id_source_bounded_presence']
    assert itemmap[20760]=={'item_table_A':False,'item_table_B':True}
    b=d['source_bounded_qualification']
    assert b['all_25_original_source_members_verified_against_original_manifest'] is True
    assert b['all_25_create_block_sha_verified_against_original_bytes'] is True
    assert b['source_2004_race_script_original_official_deployment_proven'] is False
    assert b['historical_event_evidence_distinct_from_source_script_identity'] is True
    assert b['all_QUEST04_create_refs_origin_class']=='ORIGIN_UNRESOLVED'
    assert b['original_server_execution'] is False and b['native_correct_JANKEN_warp_executed'] is False
    assert b['original_proprietary_dialogue_or_art_published'] is False
    assert b['stage_A']=='7_PARTIAL_2_OPEN' and b['stage_B_and_wiki']=='GATED' and b['R79']=='PAUSED_NON_BLOCKING' and b['overall_percent'] is None
    assert d['next'].startswith('GAMEPLAY-MECHANICS-MODULE-01')
    return True

class TestQuest04(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(INDEX.read_text('utf-8'))
        cls.char=json.loads(CHAR.read_text('utf-8'))
        cls.shards=[json.loads(p.read_text('utf-8')) for p in ITEMS]
    def test_all_25_source_refs_and_content_bounds(self):self.assertTrue(verify(self.d,self.char,self.shards))
    def negative(self, mutate):
        d=deepcopy(self.d);mutate(d)
        with self.assertRaises((AssertionError,KeyError,StopIteration)):
            verify(d,self.char,self.shards)
    def test_fabricated_janken_warp_rejected(self):self.negative(lambda d:d['source_parameter_files'][next(i for i,f in enumerate(d['source_parameter_files']) if f['template_family']=='npcgen_janken')]['losewarp_literal'].__setitem__(0,999999))
    def test_false_2004_official_script_assertion_rejected(self):self.negative(lambda d:d['source_bounded_qualification'].__setitem__('source_2004_race_script_original_official_deployment_proven',True))
    def test_false_native_runtime_rejected(self):self.negative(lambda d:d['source_bounded_qualification'].__setitem__('original_server_execution',True))
    def test_unsupported_permanent_quest_rejected(self):self.negative(lambda d:d['source_parameter_files'][0].__setitem__('origin_class','BASE_GAME_QUEST'))
    def test_race_second_itemset_difference_rejected(self):self.negative(lambda d:d['summary']['item_id_source_bounded_presence']['20760'].__setitem__('item_table_A',True))
    def test_lost_source_member_rejected(self):self.negative(lambda d:d['source_parameter_files'].pop())
    def test_false_executed_victory_rejected(self):self.negative(lambda d:d['source_bounded_qualification'].__setitem__('native_correct_JANKEN_warp_executed',True))
    def test_user_2004_article_time_not_script_time_rejected(self):self.negative(lambda d:d['source_parameter_files'][next(i for i,f in enumerate(d['source_parameter_files']) if f['template_family']=='npc_raceman')].__setitem__('source_text_date_ymd','2004-12-22 08:00'))
    def test_altered_create_sha_rejected(self):self.negative(lambda d:d['source_create_references'][0].__setitem__('source_create_block_sha256','0'*64))

if __name__=='__main__':unittest.main()
