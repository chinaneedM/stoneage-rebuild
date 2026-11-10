"""Source-bounded derived-only regression for four-village courier task cues.

No proprietary NPC scripts, DAT, sprites, itemset rows or runtime are needed.
"""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / 'research/recovered/STONEAGE-INTEGRATION48-FOUR-VILLAGE-COURIER-SOURCE-HINT-ACCEPTANCE-R1.json'
PRIOR = ROOT / 'research/recovered/STONEAGE-QUEST06-FOUR-VILLAGE-MAMMOTH-COURIER-SOURCE-R1.json'


def check_routes(d):
    scripts = {int(s['original_path'].split('_')[-1].split('.')[0]): s for s in d['source_scripts']}
    assert sorted(scripts) == [1014, 2014, 3014, 4014]
    edges = []
    for stage in (1, 2):
        accepts = {int(s[f'stage{stage}_item']):floor for floor,s in scripts.items()}
        assert len(accepts) == 4
        hints = [int(s[f'source_hint_TALKEVENT{stage + 1}_item']) for floor,s in sorted(scripts.items())]
        assert all(i in accepts for i in hints)
        counter = Counter(hints)
        miss = sorted(set(accepts).difference(counter))
        repeat = sorted(i for i,n in counter.items() if n > 1)
        x = d['source_stages_route_balance'][stage - 1]
        assert x['required_item_IDs'] == sorted(accepts)
        assert x['hint_item_occurrences'] == hints
        assert x['distinct_hint_IDs'] == sorted(counter)
        assert x['hint_duplicate_IDs'] == repeat
        assert x['acceptance_IDs_unmentioned_by_positive_hints'] == miss
        assert x['full_permutation_or_route_recovered'] is False
        for floor in sorted(scripts):
            edges.append((stage, floor, scripts[floor][f'source_hint_TALKEVENT{stage+1}_item'], accepts[scripts[floor][f'source_hint_TALKEVENT{stage+1}_item']]))
    observed = [(r['stage'],r['source_floor'],r['cue_positive_ITEM'],r['acceptance_floor_candidate']) for r in d['candidate_positive_item_cue_to_acceptance_links']]
    assert edges == observed
    assert all(r['original_travel_or_item_award_proven'] is False for r in d['candidate_positive_item_cue_to_acceptance_links'])


class TestCourierSourceLinks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(DERIVED.read_text(encoding='utf-8'))

    def test_manifest_integrity_and_history(self):
        d=self.d
        self.assertTrue(d['schema'].startswith('stoneage.integration48.'))
        self.assertEqual(d['verified_original_private_custody']['archive_sha256'],'cd26689805ad0c40e23ef934aa7c9509fe461630dd0431f7a43740abd7c91254')
        self.assertEqual(d['verified_original_private_custody']['zip_members'],13)
        self.assertTrue(d['verified_original_private_custody']['all_CRC_passed'])
        self.assertEqual(d['historical_CURRENT']['blob'],'c89e0e33537990aa2132b47c40fef49a985a935c')
        self.assertFalse(d['historical_CURRENT']['modified'])

    def test_eight_actual_npc_source_placements_four_pointers(self):
        a=self.d['source_CREATE_actors']
        self.assertEqual(len(a),8)
        self.assertEqual(sorted(x['floor'] for x in a),[1011,1014,2011,2014,3011,3014,4011,4014])
        self.assertEqual([x['create_ordinal'] for x in a],list(range(8)))
        self.assertEqual(len({x['script_path'] for x in a}),4)
        self.assertTrue(all(len(x['source_create_block_sha256'])==64 for x in a))
        self.assertEqual([x['xy'] for x in a],[[14,20],[14,20],[16,16],[16,16],[16,16],[16,16],[19,16],[19,16]])

    def test_source_six_branches_four_scripts(self):
        s=self.d['source_scripts']
        self.assertEqual(len(s),4)
        self.assertTrue(all(x['TALKEVENT_count']==6 for x in s))
        self.assertEqual([len(x['stages']) for x in s],[3]*4)
        self.assertTrue(all([x['stages'][i]['talkevent'] for i in range(3)]==[4,5,6] for x in s))
        self.assertEqual(sum(x['TALKEVENT_count'] for x in s),24)

    def test_two_stage_requirement_vectors(self):
        s=self.d['source_scripts']
        self.assertEqual([x['stage1_item'] for x in s],[2623,2622,2625,2624])
        self.assertEqual([x['stage2_item'] for x in s],[12879,4224,4212,12874])
        self.assertEqual([x['source_hint_TALKEVENT2_item'] for x in s],[2622,2623,2624,2622])
        self.assertEqual([x['source_hint_TALKEVENT3_item'] for x in s],[4224,12879,12874,4224])

    def test_independently_reconstructed_hints_and_acceptance_links(self):
        check_routes(self.d)
        self.assertEqual([x['acceptance_floor_candidate'] for x in self.d['candidate_positive_item_cue_to_acceptance_links']],[2014,1014,4014,2014,2014,1014,4014,2014])

    def test_no_invented_four_city_cycle(self):
        stages=self.d['source_stages_route_balance']
        self.assertEqual(stages[0]['acceptance_IDs_unmentioned_by_positive_hints'],[2625])
        self.assertEqual(stages[1]['acceptance_IDs_unmentioned_by_positive_hints'],[4212])
        self.assertEqual(stages[0]['hint_duplicate_IDs'],[2622])
        self.assertEqual(stages[1]['hint_duplicate_IDs'],[4224])

    def test_source_stage_levels_and_lv30_gap(self):
        for s in self.d['source_scripts']:
            self.assertEqual(s['NOFREE_guard_literal'],'LV>30')
            self.assertFalse(s['lv30_any_explicit_conditional'])
            self.assertEqual([a['level_range'] for a in s['stages']],[[1,9],[10,19],[20,29]])
        self.assertFalse(self.d['negative_evidence']['LV30_in_game_runtime_inaccessible_proven'])

    def test_original_reward_commands_as_literals_only(self):
        for s in self.d['source_scripts']:
            self.assertEqual([(x['commands']['AddGold'],x['commands']['AddExps']) for x in s['stages']], [(['1000'],['1000']),(['2000'],['16000']),(['5000'],['81000'])])
            self.assertEqual(s['stages'][0]['commands']['DelItem'],[str(s['stage1_item'])])
            self.assertEqual(s['stages'][1]['commands']['DelItem'],[f"{s['stage2_item']}*1"])
            self.assertNotIn('DelPet',s['stages'][2]['commands'])
            self.assertNotIn('GetItem',s['stages'][2]['commands'])

    def test_pet_range_is_not_item_or_deletion(self):
        self.assertEqual([x['stage3_pet_literal'] for x in self.d['source_scripts']],['1-13','1-13','1-292','1-292'])
        self.assertTrue(all(not x['source_has_DelPet'] for x in self.d['source_scripts']))
        self.assertTrue(all(not x['source_has_GetItem'] for x in self.d['source_scripts']))
        self.assertFalse(self.d['negative_evidence']['Pet_item_consumption_original_runtime_proven'])

    def test_preserved_item_identity_and_crosscarrier_boundary(self):
        it=self.d['source_items_rechecked']
        self.assertEqual(sorted(x['item_ID'] for x in it),[2622,2623,2624,2625,4212,4224,12874,12879])
        self.assertEqual(sum(bool(x['private_TW1_candidate_PNG_reverified']) for x in it),7)
        self.assertEqual(len(set(x['source_graphic_alias'] for x in it if x['private_TW1_candidate_PNG_reverified'])),6)
        self.assertFalse(next(x for x in it if x['item_ID']==2622)['private_TW1_candidate_PNG_reverified'])
        self.assertEqual(next(x for x in it if x['item_ID']==4212)['source_graphic_alias'],next(x for x in it if x['item_ID']==4224)['source_graphic_alias'])
        self.assertFalse(self.d['negative_evidence']['same_build_TW1_picture_and_mixed25_quest'])

    def test_quest31_similar_four_village_label_is_not_same_source(self):
        n=self.d['separately_verified_QUEST31_nonmerge']
        self.assertEqual(n['private_zip_sha256'],'796682fd3621a2bfecab03e7e199ca16936f95cad75f6a7842e6517f1e04dd42')
        self.assertEqual(n['private_zip_members'],26)
        self.assertEqual(n['source_create_path'],'sainasu/event/event09-12.create')
        self.assertNotEqual(n['original_source_CREATE_sha256'],self.d['verified_original_private_custody']['source_CREATE_SHA256'])
        self.assertFalse(n['same_quest_id_or_CREATE_source_as_QUEST06'])

    def test_no_original_execution_or_new_source_falsely_claimed(self):
        x=self.d['negative_evidence']
        self.assertTrue(all(v is False for v in x.values()))
        c=self.d['material_counts']
        self.assertEqual((c['new_original_DAT_files'],c['new_original_RD_decodes'],c['new_original_script_discovery'],c['proven_native_delivery_completions']),(0,0,0,0))
        self.assertEqual((self.d['stage_A']['PARTIAL'],self.d['stage_A']['OPEN']),(7,2))
        self.assertIsNone(self.d['overall_percent'])

    def test_mutated_hint_cannot_pass_as_verified_route(self):
        d=deepcopy(self.d)
        d['source_scripts'][3]['source_hint_TALKEVENT2_item']=2625
        with self.assertRaises(AssertionError):check_routes(d)
        d=deepcopy(self.d)
        d['source_stages_route_balance'][1]['acceptance_IDs_unmentioned_by_positive_hints']=[]
        with self.assertRaises(AssertionError):check_routes(d)

    @unittest.skipUnless(PRIOR.exists(),'Prior QUEST06 source catalog is verified remotely by GitHub Actions')
    def test_independent_prior_quest06_catalog_source_replay(self):
        q=json.loads(PRIOR.read_text(encoding='utf-8'))
        d=self.d
        self.assertEqual(q['summary']['source_original_CREATE_refs'],8)
        self.assertEqual(q['summary']['source_original_talkevent_count_total'],24)
        self.assertEqual(q['original_historical_CURRENT_blob_preserved'],d['historical_CURRENT']['blob'])
        for actor,prev in zip(d['source_CREATE_actors'],q['source_CREATEs']):
            self.assertEqual(actor['floor'],prev['source_floor_id'])
            self.assertEqual(actor['xy'],prev['original_borncenter'])
            self.assertEqual(actor['original_graphic_alias'],prev['source_original_graphicname'])
            self.assertEqual(actor['script_path'],prev['source_original_script_pointer'])
        for row,prev in zip(d['source_scripts'],q['source_village_scripts']):
            self.assertEqual(row['original_path'],prev['original_source_script_file'])
            self.assertEqual(row['source_sha256'],prev['original_source_script_sha256'])
            self.assertEqual([row['source_hint_TALKEVENT2_item'],row['source_hint_TALKEVENT3_item']],prev['source_initial_hint_ITEM_equal_literals'])
            for i,stage in enumerate(row['stages']):
                old=prev['source_quest_stages'][i]
                self.assertEqual(stage['talkevent'],old['talkevent'])
                self.assertEqual(stage['level_range'],old['source_level_literal_range'])
                if i<2:
                    self.assertEqual(int(stage['required_literal']),old['source_required_ITEM'])
                    self.assertEqual(stage['commands']['DelItem'][0],old['source_DelItem_literal'])
                else:
                    self.assertEqual(stage['required_literal'],old['source_required_PET_literal'])
                    self.assertFalse(old['source_DelPet_command_present'])
                self.assertEqual(int(stage['commands']['AddGold'][0]),old['AddGold_literal'])
                self.assertEqual(int(stage['commands']['AddExps'][0]),old['AddExps_literal'])
        for item,prev in zip(d['source_items_rechecked'],q['source_item_identity_and_image_qualifications']):
            self.assertEqual(item['item_ID'],prev['numeric_item_ID'])
            self.assertEqual(item['source_itemset_row_sha256'],prev['original_itemset_master_A_normalized_row_sha256'])
            self.assertEqual(item['cross_carrier_TW1_PNG_SHA256'],prev['cross_version_original_PNG_privately_verified_sha256'])


if __name__=='__main__':
    unittest.main()
