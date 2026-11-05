"""WORLD21 - rights-safe original GetPet event branch contract.

CI checks only published source-derived numeric/SHA evidence. Private original NPC
prose, original sprites and game runtime are deliberately not bundled.
"""
import json
import pathlib
import unittest
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]
RECO = ROOT / 'research' / 'recovered'


def load(filename):
    return json.loads((RECO / filename).read_text(encoding='utf-8'))


class OriginalGetPetBranchWorld21(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.new = load('STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-21-GETPET-QUEST-BRANCHES-R1.json')
        cls.g7 = load('STONEAGE-GAMEPLAY07-GETPET-NPCENEMY-ORIGINAL-SKILL-SOURCE-R1.json')
        cls.w5 = load('STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-05-GETPET-INSTANCE-TEMPLATE-SPR-R1.json')
        cls.w20 = load('STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-20-ENCOUNTER-HABITAT-SOURCE-R1.json')
        cls.w14 = load('STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-14-ORIGINAL-FISHING-QUEST-SOURCE-REPLAY-R1.json')

    def test_source_receipt_and_cross_source_git_blobs(self):
        x = self.new
        self.assertEqual(x['original_private_CHAR01_ZIP']['sha256'], self.g7['source_original_private_npc_zip']['sha256'])
        self.assertEqual(x['original_private_CHAR01_ZIP']['member_count'], 2205)
        self.assertEqual(x['original_private_CHAR01_ZIP']['member_bytes_total'], 1930332)
        self.assertTrue(x['original_private_CHAR01_ZIP']['all_member_zip_CRC_pass'])
        self.assertEqual(x['upstream_private_original_RAR_sha256'], self.w20['original_archive_sha256'])
        self.assertEqual(x['upstream_private_original_RAR_sha256'], self.w14['original_community_RAR_sha256'])
        self.assertEqual(x['original_same_archive_master_files']['enemy.txt']['sha256'], self.w20['source_files']['enemy.txt']['sha256'])
        self.assertEqual(x['original_same_archive_master_files']['enemybase.txt']['sha256'], self.w20['source_files']['enemybase.txt']['sha256'])
        self.assertEqual(x['upstream_public_index_git_blobs'], {
            'GAMEPLAY07_GetPet_numerics':'6218d88450953684dafcf19a9f85ba94d907772a',
            'WORLD05_GetPet_instance_to_template':'e4496d75236ef1050c4761fab8dcb3a2719da884',
            'WORLD20_wild_area_enemy_subgraph':'f7203fd28bc1f8cb9d1edf08d08579123df053e9'})

    def test_whole_source_census(self):
        counts = self.new['counts']
        self.assertEqual((counts['original_GetPet_source_files'],counts['original_GetPet_directive_lines'],counts['all_integer_token_occurrences_in_GetPet_raw_lines'],counts['distinct_GetPet_enemy_master_ids']), (27,29,44,36))
        self.assertEqual(counts['unique_source_event_blocks_with_GetPet'],29)
        self.assertEqual(len(self.new['source_GetPet_scripts_and_event_blocks']), 27)
        self.assertEqual(len(self.new['original_enemy_instance_to_template_lookups']),36)
        self.assertEqual(counts['ids_found_in_original_primary_enemy_master'],36)
        self.assertEqual(counts['ids_with_original_primary_template'],36)

    def test_all_original_script_and_getpet_line_sha_match_existing_private_source_custody(self):
        old = {f['original_source_relative_path']:f for f in self.g7['source_GetPet_original_NPC_files']}
        new = {f['path']:f for f in self.new['source_GetPet_scripts_and_event_blocks']}
        self.assertEqual(set(old),set(new))
        for path, item in new.items():
            self.assertEqual((item['source_bytes'],item['source_sha256'],item['source_crc32']),
                             (old[path]['original_bytes'],old[path]['source_sha256'],old[path]['source_crc32']))
            lhs = [(c['getpet_line'],c['getpet_line_sha256'],c['raw_integer_tokens_in_order']) for c in item['commands']]
            rhs = [(c['original_source_physical_line'],c['source_line_sha256'],c['source_integer_tokens_ordered']) for c in old[path]['script_commands']]
            self.assertEqual(lhs,rhs,path)

    def test_preserve_source_event_conditions_and_labels_not_infer_runtime(self):
        commands=[c for f in self.new['source_GetPet_scripts_and_event_blocks'] for c in f['commands']]
        self.assertEqual(len(commands),29)
        self.assertEqual(Counter(x for c in commands for x in c['source_type_literals']),{'ACCEPT':25,'MESSAGE':4})
        self.assertTrue(all(c['event_condition_literals'] for c in commands))
        self.assertEqual(sum('delitem' in [k['field'].lower() for k in c['raw_action_and_gate_fields']] for c in commands),22)
        self.assertEqual(sum('getitem' in [k['field'].lower() for k in c['raw_action_and_gate_fields']] for c in commands),7)
        self.assertEqual(sum('getranditem' in [k['field'].lower() for k in c['raw_action_and_gate_fields']] for c in commands),4)
        self.assertEqual(sum('endsetflg' in [k['field'].lower() for k in c['raw_action_and_gate_fields']] for c in commands),24)
        for c in commands:
            seq=[x['line'] for x in c['raw_action_and_gate_fields']]
            self.assertEqual(seq,sorted(seq))
            self.assertTrue(any(x['field'].lower()=='getpet' and x['line']==c['getpet_line'] for x in c['raw_action_and_gate_fields']))
            self.assertTrue(c['block_first_line']<=c['getpet_line']<=c['block_last_line'])

    def test_original_master_instance_to_template_not_same_integer_shortcut(self):
        old={r['source_GETPET_literal_numeric']:r for r in self.w5['GETPET_instance_template_graph']}
        new={r['getpet_integer']:r for r in self.new['original_enemy_instance_to_template_lookups']}
        self.assertEqual(set(old),set(new))
        for key, rec in new.items():
            src=old[key]
            self.assertEqual(rec['template_id_via_enemy_field4'],src['enemy_instance_A']['reference_template_id'])
            self.assertEqual(rec['enemy_master_line'],src['enemy_instance_A']['source_row_1based'])
            self.assertEqual(rec['template_master_line'],src['template_A']['source_row_1based'])
            self.assertEqual(rec['original_template_graphic_id'],src['template_A']['graphic_id'])
            self.assertEqual(rec['original_template_petflag_raw'],src['template_A']['PETFLG'])
        self.assertEqual(new[54]['template_id_via_enemy_field4'],91)
        self.assertNotEqual(new[54]['template_id_via_enemy_field4'],54)

    def test_twenty_one_reward_ids_do_not_appear_in_selected_wild_subgraph(self):
        ids={r['getpet_integer'] for r in self.new['original_enemy_instance_to_template_lookups']}
        wild={x['id'] for x in self.w20['source_enemy_instances']}
        self.assertEqual(len(wild),719)
        self.assertEqual(len(ids),36)
        self.assertFalse(wild&ids)
        self.assertEqual(self.new['negative_world20_intersection']['selected_world20_habitat_enemy_ids_hit'],[])
        self.assertTrue(self.new['negative_world20_intersection']['does_not_prove_no_other_wild_source_or_build'])
        self.assertTrue(self.new['negative_world20_intersection']['does_not_prove_historical_unobtainability'])
        self.assertTrue(all(not x['found_in_WORLD20_selected_wild_group_enemy_subgraph'] for x in self.new['original_enemy_instance_to_template_lookups']))

    def test_duplicate_reward_option_is_not_unconditionally_deduplicated(self):
        rec=next(x for x in self.new['source_GetPet_scripts_and_event_blocks'] if x['path']=='jaruga/event/oev_edb')
        self.assertEqual(rec['commands'][0]['raw_integer_tokens_in_order'],[338,360,366,482,482,78])
        self.assertEqual(rec['commands'][0]['source_type_literals'],['MESSAGE'])
        self.assertEqual(rec['commands'][0]['event_condition_literals'],['LV>0&ITEM=2564&ENDEV=2'])

    def test_old_and_active_file_candidates_are_not_conflated(self):
        paths=set(self.new['named_backup_source_paths'])
        self.assertEqual(paths,{'giiru/event/event30_5.old','quiz/equiz_04.BAK'})
        rec={x['path']:x for x in self.new['source_GetPet_scripts_and_event_blocks']}
        self.assertEqual(rec['quiz/equiz_04']['commands'][0]['raw_integer_tokens_in_order'],[351])
        self.assertEqual(rec['quiz/equiz_04.BAK']['commands'][0]['raw_integer_tokens_in_order'],[352])
        self.assertFalse(rec['quiz/equiz_04']['is_named_backup'])
        self.assertTrue(rec['quiz/equiz_04.BAK']['is_named_backup'])

    def test_quest_fishing_rod_id_2432_to_source_pet_reward_candidate(self):
        rec=next(x for x in self.new['source_GetPet_scripts_and_event_blocks'] if x['path']=='poru/team03')
        cmd=rec['commands'][0]
        self.assertEqual(cmd['raw_integer_tokens_in_order'],[333])
        self.assertEqual(cmd['event_condition_literals'],['NOWEV=64&NOWEV=57&PET=33-721&ITEM=2432'])
        actions=[(x['field'].lower(),x['value']) for x in cmd['raw_action_and_gate_fields']]
        self.assertIn(('getitem','18559'),actions)
        self.assertIn(('delitem','2432'),actions)
        self.assertIn(('endsetflg','57'),actions)
        self.assertTrue(any(str(x.get('source_original_GetItem_literal','')).startswith('2432') for x in self.w14['source_observed_branch_records']))

    def test_original_template_petflag_conflicts_are_not_discarded(self):
        rec={x['getpet_integer']:x for x in self.new['original_enemy_instance_to_template_lookups']}
        self.assertEqual([(x['GETPET_literal'],x['template_id'],x['PETFLG_A'],x['PETFLG_B']) for x in self.w5['alternate_PETFLG_conflicts']],
                         [(1479,718,1,0),(1481,719,1,0),(1483,720,1,0)])
        for key,tid in [(1479,718),(1481,719),(1483,720)]:
            self.assertEqual((rec[key]['template_id_via_enemy_field4'],rec[key]['original_template_petflag_raw']),(tid,1))

    def test_no_private_prose_runtime_or_official_claim_in_public_derivative(self):
        x=self.new
        self.assertIsNone(x['boundaries']['overall_percent'])
        self.assertFalse(x['boundaries']['GetPet_reward_delivered_in_original_runtime'])
        self.assertFalse(x['boundaries']['all_GETPET_scripts_active_at_once'])
        self.assertFalse(x['boundaries']['WORLD20_selected_wild_source_covers_every_possible_original_wild_encounter'])
        self.assertFalse(x['boundaries']['all_original_npc_files_are_official_JSS1999_TW10_CN182'])
        self.assertFalse(x['boundaries']['TW1_official_same_deployment_proven'])
        s=json.dumps(x,ensure_ascii=False)
        for forbidden in ('NomalMainMsg','ThanksMsg','PetFullMsg:','SourceFullText','source_original_dialogue_text'):
            self.assertNotIn(forbidden,s)
        self.assertFalse(any('source_text' in f for f in x['source_GetPet_scripts_and_event_blocks']))


if __name__=='__main__':
    unittest.main()
