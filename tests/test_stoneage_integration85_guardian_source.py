"""Public, original-content evidence-boundary acceptance for StoneAge INTEGRATION85.

Only consumes lawful derived numbers/SHA; never claims to exercise a proprietary
original game, original NPC interpreter, original art or privately retained data.
"""
import json
import pathlib
import re
import unittest
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / 'research/recovered/STONEAGE-INTEGRATION85-FOUR-GUARDIAN-SHRINE-ORIGINAL-2D-R1.json'
D = json.loads(PATH.read_text(encoding='utf-8'))
B = D['battle_NPCEnemy_records']
S = D['shrine_changeevent_guardian_records']
T = D['shrine_two_statue_creates']
I = D['four_magatama_and_sixteen_statue_candidate_item_source_rows']
P = D['four_source_graphic_spr_frame_pixel_receipts']
C = D['counts']
EXPECTED = {'地': (100274, 2528, 24065), '水': (100379, 2529, 24066),
            '火': (100370, 2530, 24064), '風': (100328, 2531, 24067)}


def is_sha(x):
    return isinstance(x, str) and re.fullmatch(r'[a-f0-9]{64}', x) is not None


class GuardianSourceContracts(unittest.TestCase):
    def test_01_schema_and_immutable_startup(self):
        self.assertEqual(D['schema'], 'stoneage.integration85.four_guardians_two_function_families_2d_original_source_r1')
        self.assertEqual(D['provenance']['startup_remote_main'], 'cb0626c866186b2906e33315bc860f2e993230bf')
        self.assertEqual(D['provenance']['startup_remote_tree'], '18dab1d064022f3da91e9096ac8bb75d32580b91')
        self.assertEqual(D['provenance']['historical_CURRENT_STATE_unchanged_blob'], 'c89e0e33537990aa2132b47c40fef49a985a935c')

    def test_02_independent_source_custody_not_public_binaries(self):
        x = D['provenance']
        self.assertNotEqual(x['community_mixed25_NPC_original_private_zip_sha256'], x['community_itemset_original_private_zip_sha256'])
        self.assertNotEqual(x['community_mixed25_NPC_original_private_zip_sha256'], x['separate_TW1_retail_private_PET07_html_sha256'])
        self.assertEqual((x['community_NPC_zip_members_verified_crc'], x['community_itemset_zip_members_verified_crc']), (2205, 838))
        self.assertFalse(x['original_commodity_or_client_binary_published'])

    def test_03_battle_four_per_floor_is_not_12_distinct_species(self):
        self.assertEqual(len(B), 12)
        self.assertEqual(Counter(x['floor_id'] for x in B), Counter({31603: 4, 31606: 4, 31609: 4}))
        for floor in (31603, 31606, 31609):
            self.assertEqual({x['element'] for x in B if x['floor_id'] == floor}, set(EXPECTED))

    def test_04_battle_create_original_cp950_source_spans_are_distinct(self):
        spans = [tuple(x['create_byte_span']) for x in B]
        self.assertEqual(len(set(spans)), 12)
        self.assertTrue(all(0 <= a < b <= D['source_files']['battle_create']['bytes'] for a,b in spans))
        self.assertTrue(all(is_sha(x['create_block_sha256']) for x in B))
        self.assertTrue(all(B[i]['create_byte_span'][1] <= B[i+1]['create_byte_span'][0] for i in range(11)))

    def test_05_battle_template_type_function_no_runtime_promotion(self):
        self.assertEqual(len({x['template_ref'] for x in B}), 4)
        self.assertTrue(all(x['template_functionset'] == 'NPCEnemy' for x in B))
        self.assertTrue(all(x['graphic_number'] == EXPECTED[x['element']][0] for x in B))
        self.assertTrue(all(is_sha(x['template_block_sha256']) for x in B))

    def test_06_battle_arg_paths_and_literal_numbers_not_battle_outcome(self):
        self.assertEqual(len({x['arg_source_path'] for x in B}), 12)
        self.assertTrue(all(x['arg_source_path'].startswith('npc/300/sb_4sin') and x['arg_source_path'].endswith('.arg') for x in B))
        self.assertTrue(all(len(x['arg_enemy_id_sequence_literal']) == 5 for x in B))
        self.assertTrue(all(x['arg_warp_literal'][0] == x['floor_id'] for x in B))
        self.assertTrue(all(x['arg_entype_word'] == 2 and x['arg_dieact_word'] == 1 for x in B))
        self.assertFalse(D['limitations']['NPCEnemy_original_battle_executed'])

    def test_07_enemy_ids_vary_by_floor_not_reassigned_to_9f_3f(self):
        for floor in (31603, 31606):
            self.assertEqual({x['arg_enemy_id_sequence_literal'][0] for x in B if x['floor_id']==floor},{1031,1032,1033,1034})
        self.assertEqual({x['arg_enemy_id_sequence_literal'][0] for x in B if x['floor_id']==31609}, {1048,1049,1050,1051})
        self.assertEqual({x['arg_enemy_id_sequence_literal'][1] for x in B}, {1044,1045,1046,1047})

    def test_08_source_time_and_borncenter_not_original_fps_or_collision(self):
        self.assertTrue(all(x['source_time_word']==60000 and x['source_position_borncenter'][2:]==[1,1] for x in B))
        self.assertFalse(D['limitations']['original_collision_and_path_reachability_proven'])
        self.assertFalse(D['limitations']['original_palette_selection_and_animation_timing_proven'])

    def test_09_quest_creates_four_distinct_changeevent_not_enemy(self):
        self.assertEqual(len(S), 4)
        self.assertEqual({x['element'] for x in S},set(EXPECTED))
        self.assertTrue(all(x['floor_id']==31609 and x['function_literal']=='changeevent' for x in S))
        self.assertEqual(len({x['event_source_path'] for x in S}),4)
        self.assertTrue(all(is_sha(x['event_sha256']) for x in S))

    def test_10_one_to_one_quest_element_image_item_and_branch(self):
        for x in S:
            graphic,item,_=EXPECTED[x['element']]
            self.assertEqual(x['graphic_number'],graphic)
            self.assertEqual(x['source_get_item_literal'],item)
            self.assertEqual(x['existing_item_condition_literal'],f'LV>0&ITEM={item}')
            self.assertEqual(x['source_message_branch_count'],2)

    def test_11_31609_quest_and_battle_must_not_collapse(self):
        b={x['element']:x for x in B if x['floor_id']==31609}
        self.assertEqual(len(b),4)
        for q in S:
            x=b[q['element']]
            self.assertEqual(x['graphic_number'],q['graphic_number'])
            self.assertNotEqual(x['source_position_borncenter'][:2],q['source_position_borncorner'][:2])
            self.assertNotEqual(x['template_functionset'],q['function_literal'])
            self.assertNotEqual(x['create_block_sha256'],q['create_block_sha256'])
        self.assertFalse(D['limitations']['same_floor_same_graphic_implies_same_NPC'])

    def test_12_statue_two_creates_one_source_script(self):
        self.assertEqual(len(T),2)
        self.assertEqual({x['floor_id'] for x in T},{31610})
        self.assertEqual({x['graphic_number'] for x in T},{10939,5075})
        self.assertEqual(len({x['event_source_path'] for x in T}),1)
        self.assertEqual(len({x['event_sha256'] for x in T}),1)
        self.assertNotEqual(T[0]['create_block_sha256'],T[1]['create_block_sha256'])

    def test_13_statue_four_literal_magatama_requirements_not_solved_interpreter(self):
        e=D['statue_event_literal']
        self.assertEqual(e['source_DelItem_tokens'],['2528*1','2529*1','2530*1','2531*1'])
        self.assertEqual(e['source_condition'],'LV>0&ITEM=2528*1&ITEM=2529*1&ITEM=2530*1&ITEM=2531*1')
        self.assertEqual(e['observed_source_TYPE_sequence'],['ACCEPT','MESSAGE'])
        self.assertFalse(e['native_condition_evaluation_proven'])

    def test_14_statue_original_16_candidate_items_preserve_sequence(self):
        expected=[51,52,71,148,171,241,271,375,11424,1125,684,11433,11443,11454,11463,11475]
        e=D['statue_event_literal']
        self.assertEqual(e['source_GetRandItem_candidate_ids_in_order'],expected)
        self.assertEqual(len(set(expected)),16)
        self.assertFalse(e['native_reward_selection_or_probability_proven'])

    def test_15_twenty_item_rows_and_40_full_source_line_sha(self):
        self.assertEqual(len(I),20)
        self.assertEqual({x['item_id'] for x in I}, {x[1] for x in EXPECTED.values()}|set(D['statue_event_literal']['source_GetRandItem_candidate_ids_in_order']))
        for x in I:
            self.assertEqual({v['table'] for v in x['itemset_sources']},{'itemset.txt','itemset0710.txt'})
            self.assertTrue(all(is_sha(v['original_row_sha256']) and v['line_1based']>0 for v in x['itemset_sources']))
            self.assertTrue(is_sha(x['TW1_source_RD_SHA256']))

    def test_16_magata_source_aliases_not_names_from_graphic_only(self):
        for element,(graphic,item,alias) in EXPECTED.items():
            x=next(x for x in I if x['item_id']==item)
            self.assertEqual((x['source_image_alias'],x['source_role']), (alias,'four_magatama'))
            self.assertFalse(x['two_itemset_different_column_indices_zero_based'])
        self.assertEqual(len([x for x in I if x['source_role']=='four_magatama']),4)

    def test_17_only_six_reward_id_rows_have_col_30_31_variants(self):
        changed={x['item_id'] for x in I if x['two_itemset_different_column_indices_zero_based']}
        self.assertEqual(changed,{11424,11433,11443,11454,11463,11475})
        self.assertTrue(all(x['two_itemset_different_column_indices_zero_based']==[30,31] for x in I if x['item_id'] in changed))
        self.assertTrue(all(x['itemset_sources'][0]['original_row_sha256'] != x['itemset_sources'][1]['original_row_sha256'] for x in I if x['item_id'] in changed))
        self.assertTrue(all(x['itemset_sources'][0]['original_row_sha256'] == x['itemset_sources'][1]['original_row_sha256'] for x in I if x['item_id'] not in changed))

    def test_18_twenty_items_are_not_twenty_different_pictures(self):
        self.assertEqual(len({x['source_image_alias'] for x in I}),18)
        self.assertEqual(len({x['TW1_cross_source_PNG_sha256'] for x in I}),18)
        self.assertEqual(C['source_qualifying_separate_TW1_item_PNG_aliases'],18)
        self.assertTrue(all(all(z>0 for z in x['TW1_cross_source_PNG_dimensions']) for x in I))

    def test_19_four_source_sprite_receipts_not_four_official_species(self):
        self.assertEqual(len(P),4)
        for x in P:
            self.assertEqual(x['source_numeric_graphic'],EXPECTED[x['element']][0])
            self.assertTrue(is_sha(x['PET07_original_SPR_segment_SHA256']))
            self.assertTrue(is_sha(x['source_PNG_sha256']))
            self.assertEqual(x['original_direction_code'],0)
        self.assertEqual({x['source_bitmap_no'] for x in P},{102147,113273,121571,123907})
        self.assertEqual([x['original_action_code'] for x in P if x['element']=='風'],[2])
        self.assertFalse(D['limitations']['TW1_identity_of_mixed25_named_guardians_confirmed'])

    def test_20_private_custody_only_but_manifest_complete(self):
        p=D['private_custody']
        self.assertTrue(is_sha(p['sha256']))
        self.assertEqual(p['zip_members_crc_verified'],46)
        self.assertEqual(p['non_manifest_member_sha_verified'],45)
        self.assertEqual(p['source_original_CP950_files_in_private_zip'],20)
        self.assertEqual(p['source_distinct_TW1_private_PNG_members'],22)
        self.assertTrue(p['independent_library_roundtrip_exact_zip_sha256_and_46_crc'])
        self.assertTrue(p['independent_library_roundtrip_45_individual_SHA256_verified'])
        self.assertFalse(p['local_real_original_gameplay_run'])
        self.assertFalse(D['limitations']['original_world_entered'])
        self.assertEqual(C['new_RD_decoding_in_this_work_unit'],0)

    def test_21_no_original_bytes_sneaked_into_derived_json(self):
        b=PATH.read_bytes()
        for forbidden in (b'data:image/png',b'iVBORw0KGgo',b'<!doctype html>',b'GetRandItem:51,52',b'GetItem:2528\n'):
            self.assertNotIn(forbidden,b)
        self.assertLess(len(b),85000)


if __name__=='__main__':
    unittest.main()
