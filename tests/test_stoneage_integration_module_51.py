"""INTEGRATION51: replay only public derived source-anchored indexes, not private game files."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'research' / 'recovered'
DOJO = ROOT / 'STONEAGE-INTEGRATION51-TWO-ORIGINAL-100-DOJOS-SOURCE-BRIDGE-R1.json'
OLD = ROOT / 'STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-01-DOJO-SOURCE-ATLAS-R1.json'
MAP = ROOT / 'STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json'


class TestOriginalParallelDojoSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.new = json.loads(DOJO.read_text(encoding='utf-8'))
        cls.old = json.loads(OLD.read_text(encoding='utf-8'))
        cls.maps = json.loads(MAP.read_text(encoding='utf-8'))
        cls.rows = cls.new['samdou_100_original_arg_stage_manifest']

    def test_samdou_100_source_manifest_identity(self):
        self.assertEqual(len(self.rows), 100)
        self.assertEqual([x['stage'] for x in self.rows], list(range(1, 101)))
        self.assertEqual(sum(x['original_arg_bytes'] for x in self.rows), 30872)
        self.assertEqual(len({x['original_arg_sha256'] for x in self.rows}), 100)
        for stage, item in enumerate(self.rows, 1):
            self.assertEqual(item['original_arg_path'], f'doujyou/samdou{stage:03d}.arg')
            self.assertRegex(item['original_arg_sha256'], r'^[0-9a-f]{64}$')
            self.assertRegex(item['original_create_block_sha256'], r'^[0-9a-f]{64}$')
            self.assertEqual(len(item['two_warp_create_block_sha256']), 2)
            self.assertRegex(item['original_arg_crc32'], r'^[0-9a-f]{8}$')

    def test_original_samdou_create_and_legacy_jyajyadou_sha(self):
        a = self.new['new_source_create_receipts']
        self.assertEqual(a['samdou']['sha256'], '74124b6865ed1a03b6842bba1a0be21eab03e921e67b50307257226cf921fac9')
        self.assertEqual(a['samdou']['bytes'], 43834)
        self.assertEqual(a['jyajyadou']['sha256'], self.old['npc_create']['sha256'])
        self.assertEqual(a['jyajyadou']['bytes'], self.old['npc_create']['bytes'])
        self.assertEqual(self.new['existing_original_3021_dojo_atlas']['original_git_blob_sha'],
                         '2bc01824650696131dcdd8b7e2f3b763d19e400f')

    def test_independent_old_dojo_reference_100_coordinate_and_route_matches(self):
        self.assertEqual(len(self.old['disciples']), 100)
        for row, old in zip(self.rows, self.old['disciples']):
            self.assertEqual(row['stage'], old['ordinal'])
            self.assertEqual(row['original_create_coordinate_xy'], old['coordinate'])
            self.assertEqual(row['two_original_create_warp_xy'], old['warp_positions'])
            self.assertEqual(row['arg_warp_target_floor_xy'][1:], old['configured_arg_target'][1:])
            self.assertNotEqual(row['original_arg_sha256'], old['original_arg_sha256'])
            self.assertIn(row['arg_warp_target_floor_xy'][0], (1021, 1008))

    def test_source_warp_floors_are_99_internal_plus_one_final(self):
        self.assertEqual([x['arg_warp_target_floor_xy'][0] for x in self.rows[:99]], [1021] * 99)
        self.assertEqual(self.rows[99]['arg_warp_target_floor_xy'], [1008, 20, 20])
        self.assertEqual(self.old['disciples'][99]['configured_arg_target'], [3008, 20, 20])
        self.assertEqual(self.rows[0]['arg_warp_target_floor_xy'], [1021, 400, 114])
        self.assertEqual(self.rows[9]['arg_warp_target_floor_xy'], [1021, 356, 128])
        self.assertEqual(self.rows[49]['arg_warp_target_floor_xy'], [1021, 180, 128])

    def test_source_400_static_warp_creation_counts_not_native_execution(self):
        x = self.new['cross_school_source_facts']
        self.assertEqual(x['school_source_floorIDs'], [1021, 3021])
        self.assertEqual(x['original_create_blocks_per_school'], 300)
        self.assertEqual(x['source_opponent_CREATE_per_school'], 100)
        self.assertEqual(x['source_warp_CREATE_per_school'], 200)
        self.assertEqual(x['source_two_independent_exits_per_stage'],
                         {'samdou': [1022, 1, 7], 'jyajyadou': [3022, 1, 7]})
        self.assertEqual(x['source_last_stage_floor_targets'],
                         {'samdou': [1008, 20, 20], 'jyajyadou': [3008, 20, 20]})

    def test_number_lists_are_source_lists_not_actual_enemy_species(self):
        x = self.new['cross_school_source_facts']
        self.assertEqual(x['source_enemyno_each_source_arg_list'], list(range(564, 581)))
        self.assertEqual(x['source_enemypetno_samdou_each_source_arg_list'], list(range(655, 691)))
        self.assertEqual(x['source_enemypetno_jyajyadou_each_source_arg_list'], list(range(687, 721)))
        self.assertEqual(x['numeric_pet_ID_overlap'], [687, 688, 689, 690])
        self.assertTrue(x['no_stage_runtime_reward_or_battle_result_measured'])

    def test_two_original_school_floor_MAP_distinct_not_same_graphics(self):
        rows = self.new['map_floor_original_MAP01_manifest_rows']
        l = {(x['floor'], x['format']): x for x in rows}
        self.assertEqual(len(rows), 11)
        self.assertEqual(set(l), {(f, typ) for f in (1008, 1021, 1022, 3008, 3022)
                                  for typ in ('DAT', 'MAP')} | {(3021, 'MAP')})
        self.assertEqual((l[(1021, 'DAT')]['width'], l[(1021, 'DAT')]['height']), (407, 144))
        self.assertEqual((l[(1022, 'DAT')]['width'], l[(1022, 'DAT')]['height']), (15, 15))
        self.assertEqual((l[(1008, 'DAT')]['width'], l[(1008, 'DAT')]['height']), (40, 40))
        self.assertNotEqual(l[(1021, 'MAP')]['original_sha256'], l[(3021, 'MAP')]['original_sha256'])
        self.assertNotEqual(l[(1022, 'DAT')]['original_sha256'], l[(3022, 'DAT')]['original_sha256'])
        self.assertTrue(all(x['original_DAT_bytes_reopened_this_unit'] is False for x in rows))

    def test_public_MAP01_manifest_exact_source_match(self):
        self.assertEqual(self.new['existing_MAP01_original_metadata']['original_git_blob_sha'],
                         '03675ee98d391f9ef0246315b2426f2a8b721fd3')
        old_rows = self.maps['original_decoded_source_rows']
        for x in self.new['map_floor_original_MAP01_manifest_rows']:
            hits = [r for r in old_rows if r[0] == 0 and r[5] == x['floor'] and
                    r[1].lower() == f"{x['floor']}.{x['format'].lower()}" ]
            self.assertEqual(len(hits), 1)
            r = hits[0]
            self.assertEqual((x['original_bytes'], x['original_sha256'], x['original_crc32'],
                              x['width'], x['height'], x['size_formula_valid_by_existing_MAP01']),
                             (r[2], r[3], r[4], r[6], r[7], r[8]))

    def test_old_3021_DAT_read_failure_is_not_implicitly_closed(self):
        m = self.new['existing_MAP01_original_metadata']
        self.assertEqual(m['MAP01_previous_original_3021_DAT_extraction_error_preserved'],
                         {'basename': '3021.DAT', 'expected_bytes': 351656,
                          'bytes_emitted': 327680, 'error_tag': 'File CRC error'})
        self.assertIn([0, '3021.DAT', 351656, 327680, 'File CRC error'],
                      self.maps['source_extraction_errors_not_reclassified_as_corruption'])
        self.assertTrue(m['old_3021_MAP_and_3022_DAT_verification_preserved'])

    def test_source_archive_exact_previous_scope(self):
        src = self.new['source_original_NPC_zip']
        self.assertEqual(src['bytes'], 995176)
        self.assertEqual(src['member_crc_pass_count'], 2205)
        self.assertEqual(src['sha256'], self.old['private_source_zip_sha256'])
        self.assertEqual(src['original_RAR_parent_SHA256'], self.old['private_original_rar_sha256'])
        self.assertTrue(src['all_NPC_member_bytes_reopened'])

    def test_source_disagreement_and_unknowns_cannot_be_promoted(self):
        b = self.new['negative_provenance_and_behavior_guards']
        self.assertTrue(b and all(x is False for x in b.values()))
        self.assertNotIn('ORIGINAL_TW1_OFFICIAL', self.new['evidence_scope'])
        self.assertEqual(self.new['stage_A'], '7 PARTIAL + 2 OPEN')
        self.assertEqual(self.new['stage_B'], 'GATED')
        self.assertEqual(self.new['wiki'], 'GATED')
        self.assertEqual(self.new['R79'], 'PAUSED_NON_BLOCKING')
        self.assertIsNone(self.new['overall_percent'])

    def test_current_history_preserved_and_next_is_new_material(self):
        c = self.new['historical_CURRENT']
        self.assertEqual(c['original_blob_sha'], 'c89e0e33537990aa2132b47c40fef49a985a935c')
        self.assertEqual(c['original_size_bytes'], 2709173)
        self.assertTrue(c['full_native_Git_blob_text_read_this_turn'])
        self.assertFalse(c['original_file_changed'])
        self.assertIn('different available source-qualified original scene/content', self.new['next'])


if __name__ == '__main__':
    unittest.main()
