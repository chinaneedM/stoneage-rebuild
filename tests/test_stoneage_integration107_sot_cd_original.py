"""Metadata-only replay; never ships private community scripts or commercial art."""
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
P = ROOT / 'research/recovered/STONEAGE-INTEGRATION107-SOT-CD-27-ORIGINAL-SOURCE-VS-O14-R1.json'
O14 = ROOT / 'research/recovered/STONEAGE-O14-SOT-CD-2003-PLAYER-SOURCE-R1.json'
MAP = ROOT / 'research/recovered/STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json'


class OriginalSotCDSourceBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(P.read_text(encoding='utf-8'))
        cls.old = json.loads(O14.read_text(encoding='utf-8'))
        cls.map_index = json.loads(MAP.read_text(encoding='utf-8'))
        cls.rows = cls.report['rows']

    def test_private_source_custody_is_a_pointer_only(self):
        q = self.report['custody']
        self.assertEqual((q['private_original_NPC_zip_bytes'], q['private_original_NPC_zip_crc_members']), (995176, 2205))
        self.assertEqual(q['original_create_bytes'], 4719)
        self.assertEqual(q['original_handler_files_unique_verified'], 27)
        self.assertRegex(q['original_create_sha256'], r'^[a-f0-9]{64}$')
        self.assertEqual(self.report['baseline']['immutable_CURRENT_blob'], 'c89e0e33537990aa2132b47c40fef49a985a935c')

    def test_all_27_byte_spans_and_hashes(self):
        self.assertEqual(len(self.rows), 27)
        self.assertEqual([r['ordinal'] for r in self.rows], list(range(27)))
        self.assertEqual(len({r['original_block_sha256'] for r in self.rows}), 27)
        self.assertEqual(len({r['original_handler_path'] for r in self.rows}), 27)
        self.assertEqual(len({r['original_handler_sha256'] for r in self.rows}), 27)
        self.assertTrue(all(re.fullmatch(r'[0-9a-f]{64}', r['original_handler_sha256']) for r in self.rows))
        self.assertTrue(all(r['source_type'] == 'changeevent' for r in self.rows))
        self.assertTrue(all(0 <= a < b <= 4719 for a, b in (r['source_byte_span'] for r in self.rows)))
        self.assertEqual([r['source_byte_span'][0] for r in self.rows], sorted(r['source_byte_span'][0] for r in self.rows))

    def test_all_24_O14_checkpoint_coordinates_live_in_separate_evidence_layers(self):
        for route in ('C', 'D'):
            group = [r for r in self.rows if r['route'] == route]
            self.assertEqual(len(group), 12)
            for i, row in enumerate(group):
                old = self.old['checkpoints'][route][i]
                self.assertEqual(row['sequence'], i + 1)
                self.assertEqual(row['O14_2003_guide_xy'], [old['local_coordinate']['east'], old['local_coordinate']['south']])
                self.assertIsNone(old['historical_map_floor_id'])
                self.assertEqual(row['source_minus_guide_xy'], [a-b for a, b in zip(row['source_xy'], row['O14_2003_guide_xy'])])
        self.assertEqual(self.rows[0]['source_xy'], [33, 56])
        self.assertEqual(self.rows[25]['O14_2003_guide_xy'], [108, 29])
        self.assertEqual(self.rows[25]['source_xy'], [108, 28])
        self.assertEqual(self.rows[26]['source_xy'], [88, 116])

    def test_keep_six_original_discrepancies_and_19_equal_checkpoints(self):
        differences = [(r['route'], r['sequence']) for r in self.rows if r['route'] and not r['exact_same_xy_as_2003_guide']]
        self.assertEqual(differences, [('C', 3), ('D', 2), ('D', 3), ('D', 4), ('D', 5)])
        self.assertEqual(sum(r['exact_same_xy_as_2003_guide'] for r in self.rows if r['route']), 19)
        self.assertEqual(len(self.report['source_vs_2003_guide_inequalities']), 6)
        self.assertEqual(self.rows[3]['source_minus_guide_xy'], [-6, -34])

    def test_original_script_token_membership_is_not_runtime_execution(self):
        q = self.report['checkpoint_handoff_numeric_probes']
        self.assertEqual(len(q), 24)
        self.assertTrue(all(x['source_script_gets_expected_next_ID'] and x['source_script_deletes_prior_ID'] for x in q))
        self.assertEqual([x['expected_next_get_ID'] for x in q[:12]], list(range(2576, 2588)))
        self.assertEqual([x['expected_deleted_ID'] for x in q[12:]], list(range(2575, 2587)))
        self.assertIn(48, self.rows[25]['original_GetPet_numeric_IDs'])
        self.assertIn(76, self.rows[26]['original_GetPet_numeric_IDs'])
        self.assertTrue(self.report['historic_boundary']['source_2003_guide_are_player_submission_not_native'])
        self.assertFalse(self.report['historic_boundary']['native_reward_probability_or_reset_executed'])

    def test_prior_source_DAT_geometry_uses_exact_previous_catalog(self):
        m = self.map_index
        cols = m['original_decoded_source_columns']
        idx = {r[cols.index('numeric_floor_name_or_null')]: r for r in m['original_decoded_source_rows']
               if r[cols.index('group_code')] == 0 and
               r[cols.index('source_relative_path')].upper().endswith('.DAT') and
               r[cols.index('header_width_candidate_or_null')] and r[cols.index('header_height_candidate_or_null')]}
        c = {'WITHIN_PRIOR_DAT_DIMENSIONS': 0, 'OUTSIDE_PRIOR_DAT_DIMENSIONS': 0, 'NO_QUALIFIED_DAT': 0}
        for r in self.rows:
            dat = idx.get(r['floor'])
            if dat is None:
                self.assertEqual(r['prior_DAT_geometry'], 'NO_QUALIFIED_DAT')
                self.assertIsNone(r['prior_DAT_dimensions'])
            else:
                dim = [dat[cols.index('header_width_candidate_or_null')], dat[cols.index('header_height_candidate_or_null')]]
                self.assertEqual(r['prior_DAT_dimensions'], dim)
                expected = ('WITHIN_PRIOR_DAT_DIMENSIONS' if 0 <= r['source_xy'][0] < dim[0] and 0 <= r['source_xy'][1] < dim[1]
                            else 'OUTSIDE_PRIOR_DAT_DIMENSIONS')
                self.assertEqual(r['prior_DAT_geometry'], expected)
            c[r['prior_DAT_geometry']] += 1
        self.assertEqual(c, {'WITHIN_PRIOR_DAT_DIMENSIONS': 17, 'OUTSIDE_PRIOR_DAT_DIMENSIONS': 0, 'NO_QUALIFIED_DAT': 10})

    def test_no_new_native_certification_or_commercial_text(self):
        lim = self.report['historic_boundary']
        self.assertFalse(lim['TW1_or_original_official_same_server_deployment_proven'])
        self.assertFalse(lim['original_client_world_executed'])
        self.assertFalse(lim['proprietary_original_script_or_text_committed_publicly'])
        self.assertTrue(lim['map_DIMENSIONS_only_prior_manifest_no_new_DAT_bytes_read'])
        s = P.read_text(encoding='utf-8')
        for forbidden in ('有太陽的時候', '玩家一定', '官方同服已证', 'GetRandItem probability'):
            self.assertNotIn(forbidden, s)


if __name__ == '__main__':
    unittest.main()
