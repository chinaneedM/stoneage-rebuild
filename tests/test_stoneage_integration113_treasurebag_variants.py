"""Evidence-only regression: two different preserved treasurebag source schemes.

Never imports private original ZIP, images, or native game code in public CI.
"""
import collections
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'research' / 'recovered'
REPORT = ROOT / 'STONEAGE-INTEGRATION113-TREASUREBAG-VARIANTS-ORIGINAL-SOURCE-R1.json'
CHAR = ROOT / 'STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
ENEMY = ROOT / 'STONEAGE-CHARACTER-NPC-MODULE-09-ORIGINAL-NPCENEMY-ROSTER-BRIDGE-R1.json'
QUEST = ROOT / 'STONEAGE-QUEST19-MARJU-POST-TREASUREBAG-SOURCE-R1.json'
SCENE = ROOT / 'STONEAGE-SCENE28-TW10-ACTION1-PIXELS-R1.json'


class TreasurebagSourceVariants(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(REPORT.read_text(encoding='utf-8'))
        cls.c = json.loads(CHAR.read_text(encoding='utf-8'))
        cls.e = json.loads(ENEMY.read_text(encoding='utf-8'))
        cls.q = json.loads(QUEST.read_text(encoding='utf-8'))
        cls.s = json.loads(SCENE.read_text(encoding='utf-8'))

    def test_precise_base_and_private_archive_qualified(self):
        b, p = self.r['baseline'], self.r['carrier']
        self.assertEqual(b['main'], '7cd3601bfe0fefd2861bfbc964b1e23b8a85812e')
        self.assertEqual(b['tree'], 'd6700ad0bbea95cbcac013915581ddd6c03e11b8')
        self.assertEqual(b['main_actions_completed_success'], 26)
        self.assertEqual((b['preserved_CURRENT_bytes'], b['preserved_CURRENT_blob']),
                         (2709173, 'c89e0e33537990aa2132b47c40fef49a985a935c'))
        self.assertEqual(p['private_NPC_archive_bytes'], 995176)
        self.assertEqual(p['private_NPC_archive_member_CRC_all_pass'], 2205)
        self.assertEqual(p['private_NPC_archive_SHA256'],
                         'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f')
        self.assertTrue(p['seven_original_files_actually_re_read_and_SHA_matched'])

    def test_all_seven_exact_original_source_file_receipts_and_CP950_negative(self):
        files = self.r['carrier']['files']
        old = {a[0]: a for a in self.c['source_files']}
        self.assertEqual(len(files), 7)
        self.assertEqual(set(x['path'] for x in files),
                         {'100/sb_mimi.create', '100/sb_mimi.template', '100/sb_mimi.arg',
                          '300/sb_hag.template', '300/sb_hag.create', '300/sb_hag.arg',
                          'extra/event/marju.create'})
        for f in files:
            a = old[f['path']]
            self.assertEqual((f['bytes'], f['sha256'], f['crc32']),
                             tuple(a[1:4]), f['path'])
        self.assertIn('undecodable CP950 byte',
                      self.r['carrier']['original_CP950_roundtrip_note'])

    def test_all_twelve_original_byte_windows_and_same_arg_template_pointer(self):
        rows = self.r['sb_mimi_variant']['raw_original_create_blocks']
        self.assertEqual(len(rows), 12)
        for r in rows:
            index = next(a for a in self.c['create_rows']
                         if a[0] == r['source_create_file']
                         and a[1] == r['source_block_ordinal'])
            self.assertEqual(r['source_raw_byte_window'], index[2:4])
            self.assertEqual(r['source_raw_block_sha256'], index[4])
            self.assertEqual(r['floor'], index[5])
            self.assertEqual(r['source_borncenter'], index[8])
            self.assertEqual(r['source_graphic_alias'], index[6])
            self.assertEqual(r['source_function_token'], index[11])
            self.assertEqual(index[15][0][0], r['source_arg_file'])
            self.assertEqual(index[15][0][2], r['source_arg_SHA256'])
            ref = next(a for a in self.e['create_refs']
                       if a[0] == r['source_create_file']
                       and a[1] == r['source_block_ordinal'])
            self.assertEqual(ref[2], r['source_raw_block_sha256'])
            self.assertEqual(ref[4], r['source_template_file'])
            self.assertEqual(ref[6], r['source_template_block_sha256'])
            self.assertEqual(ref[7], r['source_arg_file'])
            self.assertEqual(ref[8], r['source_arg_SHA256'])
        self.assertEqual(collections.Counter(r['floor'] for r in rows), {122:6,118:6})
        self.assertEqual(set(r['source_graphic_alias'] for r in rows), {16073})
        self.assertEqual(len({(r['floor'], *r['source_borncenter'][:2]) for r in rows}), 12)

    def test_literal_arg_enemy_1117_and_distinct_template_key_are_not_rewritten(self):
        v = self.r['sb_mimi_variant']
        arg = next(a for a in self.e['argument_files']
                   if a[0] == v['source_arg_file'])
        self.assertEqual(arg[3], [1117]*10)
        self.assertEqual(arg[5], [2697])
        self.assertEqual(arg[2], 268)
        p = v['original_literal_arg']
        self.assertEqual((p['entype'], p['item'], p['time'], p['dieact']), (2,2697,60,0))
        self.assertEqual(p['enemyno'], [1117]*10)
        t = v['function_template_resolution']
        self.assertEqual(t['create_function_token'], 'sb_hag')
        self.assertEqual(t['actual_matching_template_file'], '300/sb_hag.template')
        self.assertEqual(t['unreferenced_same_dir_template_key'], 'sb_mimi')
        self.assertEqual(t['source_template_names']['sb_hag']['create_ref_count_in_public_index'], 13)
        self.assertEqual(t['source_template_names']['sb_mimi']['create_ref_count_in_public_index'], 0)
        for name in ['sb_hag', 'sb_mimi']:
            found = [x for x in self.c['template_rows'] if x[3] == name]
            self.assertEqual(len(found), 1)
            expected = t['source_template_names'][name]
            self.assertEqual((found[0][0], found[0][2], found[0][4]),
                             (expected['path'], expected['raw_block_sha256'],
                              expected['source_functionset']))
        self.assertTrue(t['native_type_selector_UNVERIFIED'])

    def test_prior_quest19_ten_distinct_scripted_bags_one_exact_collision(self):
        q, v = self.q, self.r['prior_QUEST19_comparison']
        bag = [x for x in q['npc_placements']
               if x['script'] not in ('extra/event/marju','extra/event/marju01')]
        self.assertEqual(len(bag), 10)
        self.assertEqual(v['existing_quest19_bag_NPCs'], 10)
        self.assertEqual(q['script_lifecycle_literal']['bag_accept_predicates'],
                         ['LV>0','ITEM=2697'])
        self.assertEqual(len(self.c['create_rows']), 4985)
        qcreate = [x for x in self.c['create_rows']
                   if x[0] == 'extra/event/marju.create']
        self.assertEqual(len(qcreate), 12)
        self.assertEqual({x[11] for x in qcreate}, {'changeevent'})
        overlaps = [(x['floor'], x['source_borncenter'][:2], x['source_block_ordinal'], y['script'])
                    for x in self.r['sb_mimi_variant']['raw_original_create_blocks']
                    for y in bag
                    if x['floor'] == y['floor']
                    and x['source_borncenter'][:2] == y['spawn_xy']]
        self.assertEqual(overlaps, [(122,[162,12],5,'extra/event/marju04a')])
        self.assertEqual(v['exact_spawn_coordinate_collisions'],
                         [{'floor':122,'xy':[162,12],'sb_mimi_ordinal':5,
                           'other_original_quest19_script':'extra/event/marju04a',
                           'graphic_alias':16073}])
        self.assertTrue(v['distinct_source_CREATE_config_rows_must_not_be_summed_to_native_world_bag_count'])

    def test_1117_original_community_enemy_to_TW1_SPR_numeric_candidate(self):
        p = self.r['enemy_instance_and_original_visual_bridge']
        row = next(a for a in self.e['source_enemy_number_to_paired_template_and_spr']
                   if a[0] == 1117)
        self.assertEqual(row[:4], [1117,3,100252,1])
        self.assertEqual(row[4], p['preserved_community_SPR_index'])
        self.assertEqual(row[6], 56)
        self.assertFalse(p['community_two_enemy_instance_rows_exact_same_SHA'])
        self.assertFalse(p['community_two_enemy_template_rows_exact_same_SHA'])
        src = next(x for x in self.s['same_segment_as_R40_preserved_mixed25']
                   if x['graphic'] == 100252)
        self.assertEqual(src['whole_spr_segment_sha256'],
                         p['TW10_original_SPR_graphic100252_segment_sha256'])
        self.assertEqual(src['tw10_source_group_index'], 242)
        self.assertEqual(p['previously_verified_original_TW10_action1_direction_sequences'], 8)
        self.assertEqual(p['previously_verified_original_TW10_action1_frame_occurrences'], 16)
        self.assertEqual(p['private_SCENE28_observer_zip_sha256'],
                         self.s['private_observation_artifact']['sha256'])
        self.assertTrue(p['same_SPR_segment_does_not_prove_original_same_deployment_or_same_RD_pixels'])

    def test_both_source_floor_geometry_limits_and_nonpromotion(self):
        q = self.q['treasurebag_npc_relocation']
        p = self.r['map_bounds_reuse']
        self.assertEqual(p['source_QUEST19_map_118'], q['MAP09_118'])
        self.assertEqual(p['source_QUEST19_map_122'], q['MAP09_122'])
        self.assertEqual(q['MAP09_118']['geometry'], [250,180])
        self.assertEqual(q['MAP09_122']['geometry'], [300,200])
        self.assertTrue(p['all_12_xy_within_prior_original_source_geometries'])
        for x in self.r['sb_mimi_variant']['raw_original_create_blocks']:
            w,h = q['MAP09_118']['geometry'] if x['floor']==118 else q['MAP09_122']['geometry']
            self.assertTrue(0<=x['source_borncenter'][0]<w)
            self.assertTrue(0<=x['source_borncenter'][1]<h)
        counts = self.r['counts']
        self.assertEqual((counts['new_original_source_files_discovered'],
                          counts['original_NPC_CREATES_byte_windows_re_verified'],
                          counts['exact_coordinate_collisions'],
                          counts['new_original_TW10_RD_blocks_read'],
                          counts['new_original_native_game_client_server_execution']),
                         (0,12,1,0,0))
        self.assertGreaterEqual(len(self.r['negative_limits']), 6)
        self.assertTrue(all(x['floor'] in (118,122)
                            for x in self.r['sb_mimi_variant']['raw_original_create_blocks']))


if __name__ == '__main__':
    unittest.main()
