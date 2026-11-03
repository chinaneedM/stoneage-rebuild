"""QUEST01 archival index integrity. Public CI never opens or executes proprietary commercial originals."""
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'research' / 'recovered'
INDEX = ROOT / 'STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json'
SHARDS = [ROOT / 'item-module-01' / f'STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{i:02d}-R1.json' for i in range(1, 8)]
HEX = re.compile(r'^[0-9a-f]{64}$')


def verify(j,shards):
    assert j['schema'] == 'stoneage.quest_story_module01_original_changeevent_block_graph.r1'
    src = j['source']
    assert (src['original_RAR_bytes'], src['RAR_total_files'], src['original_NPC_files_verified'], src['original_NPC_bytes_verified']) == (361255180, 7952, 2205, 1930332)
    assert src['all_NPC_physical_size_SHA_CRC_replayed'] is True
    assert HEX.fullmatch(src['original_RAR_sha256'])
    assert src['all_create_braced_blocks'] == 5005 and src['all_creates_with_enemy'] == 4985
    assert src['create_cp950_replacement_needed_files'] == len(src['create_cp950_replacement_source_paths_sha256']) == 5
    assert all(HEX.fullmatch(x) for x in src['create_cp950_replacement_source_paths_sha256'])
    assert src['qualifying_template_literal'] == 'changeevent' and HEX.fullmatch(src['qualifying_template_source_sha256'])
    creates = j['source_creation_references']
    scripts = j['source_scripts']
    blocks = j['source_event_blocks']
    assert (len(creates),len(scripts),len(blocks)) == (315,295,1349)
    assert (j['source_create_references_count'], j['source_script_distinct_count'], j['event_blocks_anchored_on_actual_TYPE']) == (315,295,1349)
    assert j['source_script_total_bytes'] == sum(x['original_size'] for x in scripts) == 434873
    assert j['source_create_paths_count'] == len({x['create_source_path'] for x in creates}) == 51
    sdict = {x['path']:x for x in scripts}
    assert len(sdict) == 295
    ccount = Counter()
    assert j['origin_class_distribution_on_create_references'] == {'UNRESOLVED':315,'VERIFIED_PERMANENT_ORIGINAL':0,'VERIFIED_TIME_LIMITED_EVENT':0}
    for c in creates:
        assert c['origin_class']=='UNRESOLVED'
        assert c['original_script_path'] in sdict
        assert c['original_script_sha']==sdict[c['original_script_path']]['original_sha256']
        assert HEX.fullmatch(c['create_source_sha'])
        assert isinstance(c['floorid'],int)
        assert isinstance(c['create_brace_ordinal'],int) and c['create_brace_ordinal']>=0
        ccount[c['original_script_path']]+=1
    for s in scripts:
        assert s['quest_origin']=='UNRESOLVED'
        assert s['create_source_references']==ccount[s['path']]
        assert HEX.fullmatch(s['original_sha256']) and re.fullmatch('[0-9a-f]{8}',s['original_crc32'])
    controls = Counter()
    types = Counter()
    blockcounts=defaultdict(Counter)
    events = set()
    event_edges=set()
    keywords=Counter()
    item_ids=set()
    seen=set()
    end_count=0
    for b in blocks:
        key=(b['script_path'],b['script_block_ordinal'])
        assert key not in seen
        seen.add(key)
        assert b['script_path'] in sdict
        assert b['source_file_sha']==sdict[b['script_path']]['original_sha256']
        assert b['origin_class']=='UNRESOLVED'
        assert b['raw_type'] in ('MESSAGE','ACCEPT','REQUEST','CLEAN')
        assert HEX.fullmatch(b['source_section_decoded_cp950_normalized_UTF8_sha256'])
        assert HEX.fullmatch(b['condition_expression_decoded_cp950_UTF8_sha256'])
        assert b['condition_present'] in (True,False)
        end_count+=int(b['source_End_found'])
        types[b['raw_type']]+=1
        blockcounts[b['script_path']][b['raw_type']]+=1
        keywords.update(b['condition_keywords'])
        for k,v in b['item_numeric_refs'].items():
            assert k in ('predicate_ITEM','GetItem','DelItem','GetRandItem','GetStone')
            assert v==sorted(set(v))
            if k!='GetStone':item_ids.update(v)
        if b['event_number'] is not None:
            assert b['event_number'] in b['event_number_literals']
            if b['event_number']>=0:events.add(b['event_number'])
            for f in b['end_set_flags']:event_edges.add((b['event_number'],f))
        for token,count in b['condition_keywords'].items():
            assert token in ('ITEM','LV','PET','NOWEV','ENDEV','TRANS','STONE','FAME','GOLD','FLOOR','TIME','DAY','MONTH','YEAR')
            assert count>=0
        assert b['source_type_line']>=1
    assert end_count==1348
    assert dict(sorted(types.items()))==j['event_block_TYPE_totals']=={'ACCEPT':494,'CLEAN':5,'MESSAGE':769,'REQUEST':81}
    assert sum(x['source_control_lines']['TYPE'] for x in scripts)==len(blocks)
    assert j['script_control_lines_totals']=={'EventNo':1348,'TYPE':1349,'EVENT':1349,'EventEnd':1348}
    assert j['source_EventEnd_count_provenance']=={'CP950_Unicode_trimmed_EventEnd_lines':1348,'original_raw_exact_ASCII_EventEnd_lines':1346,'original_one_ASCII_trailing_space':1,'original_one_CP950_fullwidth_trailing_space':1,'CHAR08_previous_report_count':1347,'different_original_line_matching_not_source_change':True}
    assert all(dict(sorted(blockcounts[s['path']].items()))==s['actual_block_type_counts'] for s in scripts)
    assert j['actual_original_event_number_nonnegative_distinct']==len(events)==59
    assert j['actual_original_event_number_value_list']==sorted(events)
    assert [list(x) for x in sorted(event_edges)]==j['literal_EndSetFlg_number_pairs']
    assert len(event_edges)==63
    assert dict(sorted(keywords.items()))==j['original_source_predicate_token_occurrences']
    assert len(j['anomalous_source_script_controls'])==2
    assert {x['path'] for x in j['anomalous_source_script_controls']}=={'giiru/event/garunaev6','poru/titan'}
    itemA=set();itemB=set()
    for shard in shards:
        for row in shard['rows']:
            itemB.add(row[0]);
            if row[1] is not None:itemA.add(row[0])
    assert (len(itemA),len(itemB))==(13254,13915)
    ref=j['item_references_from_parsed_event_blocks']
    assert len(item_ids)==ref['distinct_item_numeric_IDs']==694
    assert sorted(item_ids&itemA)==ref['both_tables']
    assert sorted(item_ids&(itemB-itemA))==ref['later_table_only']==[2054,2391,20570,20571,20572]
    assert sorted(item_ids-itemB)==ref['missing_both_tables']==[2744,2745]
    assert len(ref['both_tables'])==687
    assert all(HEX.fullmatch(x) for x in ref['source_candidate_tables_sha256'])
    bounds=j['bounds']
    for k in ('source_CREATE_cp950_replacements_not_imputed_to_original_script_text','source_EventNo_not_proven_server_flow','source_EndSetFlg_not_proven_quest_completion','source_ITEM_tokens_not_proven_item_redeemed','source_path_event_label_not_proven_operated_holiday_event','source_create_references_not_distinct_quests','not_official_TW10_or_CN182_same_deployment','no_original_commercial_script_lines_or_dialogue_in_public_git'):
        assert bounds[k] is True
    assert bounds['native_client_or_server_quest_execution_observed'] is False
    assert bounds['full_official_historical_quest_population_closed'] is False
    assert bounds['overall_percent'] is None
    assert bounds['stage_A']=='7_PARTIAL_2_OPEN' and bounds['stage_B_and_wiki']=='GATED' and bounds['R79']=='PAUSED_NON_BLOCKING'
    assert j['next'].startswith('QUEST_STORY_MODULE_02')
    return True

class TestQuest01(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.j=json.loads(INDEX.read_text('utf-8'))
        cls.shards=[json.loads(p.read_text('utf-8')) for p in SHARDS]
    def test_complete_315_create_295_script_1349_block_replay(self):self.assertTrue(verify(self.j,self.shards))
    def test_origin_must_remain_unresolved(self):
        j=deepcopy(self.j);j['source_creation_references'][0]['origin_class']='OFFICIAL_PERMANENT'
        with self.assertRaises(AssertionError):verify(j,self.shards)
    def test_event_label_is_not_a_holiday_proof(self):
        j=deepcopy(self.j);j['bounds']['source_path_event_label_not_proven_operated_holiday_event']=False
        with self.assertRaises(AssertionError):verify(j,self.shards)
    def test_block_type_fabrication_rejected(self):
        j=deepcopy(self.j);j['source_event_blocks'][0]['raw_type']='REWARD_CLAIM'
        with self.assertRaises(AssertionError):verify(j,self.shards)
    def test_phantom_item_reward_rejected(self):
        j=deepcopy(self.j);j['source_event_blocks'][0]['item_numeric_refs']['GetItem']=[999999999]
        with self.assertRaises(AssertionError):verify(j,self.shards)
    def test_fake_quest_runtime_rejected(self):
        j=deepcopy(self.j);j['bounds']['native_client_or_server_quest_execution_observed']=True
        with self.assertRaises(AssertionError):verify(j,self.shards)
    def test_legacy_1347_EventEnd_not_silently_preserved(self):
        j=deepcopy(self.j);j['script_control_lines_totals']['EventEnd']=1347
        with self.assertRaises(AssertionError):verify(j,self.shards)
    def test_script_sha_source_mismatch_rejected(self):
        j=deepcopy(self.j);j['source_creation_references'][0]['original_script_sha']='0'*64
        with self.assertRaises(AssertionError):verify(j,self.shards)

if __name__=='__main__':unittest.main()