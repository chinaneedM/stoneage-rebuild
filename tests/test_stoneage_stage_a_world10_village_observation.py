"""Verify public WORLD10 joins without reading private original media."""

import json
from collections import Counter
from pathlib import Path
import re
import unittest


RECOVERED = Path(__file__).resolve().parents[1] / 'research' / 'recovered'
WORLD04 = 'STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-04-THREE-VILLAGE-NPC-TEXT-SOURCE-R1.json'
WORLD10 = 'STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-10-THREE-VILLAGE-MAP-OBSERVATION-R1.json'
RAR_REPLAY = 'STONEAGE-STAGE-A-INDEPENDENT-RAR-MAP-PIXEL-RECOVERY-R1.json'
HEX_SHA256 = re.compile(r'[0-9a-f]{64}')


def read_report(name):
    return json.loads((RECOVERED / name).read_bytes())


class VillageObservation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world04 = read_report(WORLD04)
        cls.world10 = read_report(WORLD10)
        cls.prior_rar_replay = read_report(RAR_REPLAY)

    def test_same_archive_members_match_prior_verified_bytes(self):
        report = self.world10
        self.assertEqual(report['original_archive_sha256'], self.prior_rar_replay['archive']['sha256'])
        self.assertEqual(report['original_archive_sha256'], self.world04['original_npc_carrier']['original_RAR_sha256'])
        self.assertEqual(set(report['image_sources']), {'adrn_15.bin', 'real_15.bin', 'Palet_1.sap'})
        for name, member in report['image_sources'].items():
            prior = self.prior_rar_replay['source_art_and_dojo_config'][name]
            self.assertEqual({k: member[k] for k in prior}, prior)
            self.assertTrue(member['archive_member'].endswith('/' + name))
        prior_floors = self.world04['floor_original_DAT_receipts']
        for floor, prior in zip(report['floors'], prior_floors, strict=True):
            member = floor['original_DAT']
            self.assertEqual(floor['floor'], prior['floor'])
            self.assertEqual(floor['dimensions'], prior['dimensions'])
            self.assertEqual(member['bytes'], prior['original_DAT_bytes'])
            self.assertEqual(member['crc32'], prior['original_DAT_crc32'])
            self.assertEqual(member['sha256'], prior['original_DAT_sha256'])
            self.assertEqual(len(member['plane_sha256_little_endian']), 3)
            self.assertTrue(all(HEX_SHA256.fullmatch(h) for h in member['plane_sha256_little_endian']))

    def test_all_47_source_anchors_keep_exact_identity_and_order(self):
        source = self.world04['rows']
        result = [(floor['floor'], row) for floor in self.world10['floors'] for row in floor['anchors']]
        self.assertEqual(len(result), 47)
        self.assertEqual(Counter(row['role'] for _, row in result), {'TownPeople': 35, 'SignBoard': 12})
        self.assertEqual(len({(floor, *row['coordinate']) for floor, row in result}), 47)
        for (floor, actual), prior in zip(result, source, strict=True):
            self.assertEqual(floor, prior['floor'])
            self.assertEqual(actual['coordinate'], prior['position'])
            self.assertEqual(actual['role'], prior['role'])
            self.assertEqual(actual['create_path'], prior['source_CREATE_path'])
            self.assertEqual(actual['create_ordinal'], prior['source_CREATE_ordinal'])
            self.assertEqual(actual['arg_sha256'], prior['original_arg_sha256'])
            self.assertEqual(len(actual['source_cell_u16']), 3)
            self.assertTrue(all(type(value) is int and 0 <= value <= 65535 for value in actual['source_cell_u16']))
            self.assertNotIn('text', actual)
        for floor in self.world10['floors']:
            values = Counter(row['source_cell_u16'][2] for row in floor['anchors'])
            self.assertEqual(values, {49152: len(floor['anchors'])})
            self.assertEqual(floor['anchor_event_values'], [[49152, len(floor['anchors'])]])
        self.assertEqual(self.world10['npc_archive_replay']['unique_CREATE_files'], 11)
        self.assertEqual(self.world10['npc_archive_replay']['unique_ARG_files'], 47)
        self.assertEqual(self.world10['npc_archive_replay']['verified_CREATE_blocks'], 47)

    def test_census_and_crop_conservation(self):
        for floor in self.world10['floors']:
            width, height = floor['dimensions']
            x0, y0, x1, y1 = floor['window_inclusive']
            self.assertTrue(0 <= x0 <= x1 < width and 0 <= y0 <= y1 < height)
            self.assertTrue(all(x0 <= x <= x1 and y0 <= y <= y1 for x, y in
                                (row['coordinate'] for row in floor['anchors'])))
            full = floor['full_floor_census']
            window = floor['window_census']
            for scope in (full, window):
                self.assertEqual(scope['candidate_occurrences'], scope['decoded_occurrences']
                                 + sum(row[1] for row in scope['missing'] + scope['ambiguous']))
                self.assertEqual(scope['candidate_aliases'], scope['decoded_aliases']
                                 + len(scope['missing']) + len(scope['ambiguous']))
                self.assertTrue(all(len(row[2]) >= 2 for row in scope['ambiguous']))
            self.assertLessEqual(window['candidate_occurrences'], full['candidate_occurrences'])
            self.assertLessEqual(window['candidate_aliases'], full['candidate_aliases'])
            self.assertEqual(floor['observation_png']['drawn_RD_placements'], window['decoded_occurrences'])
        # Independent prior recovery is a frozen cross-check for the most fragile DAT.
        old_3000 = self.prior_rar_replay['same_archive_map_graphics']['floor_candidate_pixels']['3000']
        census_3000 = next(x['full_floor_census'] for x in self.world10['floors'] if x['floor'] == 3000)
        self.assertEqual(census_3000['candidate_aliases'], old_3000['unique_draw_candidate_aliases'])
        self.assertEqual(census_3000['decoded_aliases'], old_3000['unique_dual_decoded_aliases'])
        self.assertEqual(census_3000['candidate_occurrences'], old_3000['total_occurrences'])
        self.assertEqual(census_3000['decoded_occurrences'], old_3000['decoded_occurrences'])

    def test_private_archive_and_historical_boundaries(self):
        report = self.world10
        package = report['private_observer']
        self.assertTrue(HEX_SHA256.fullmatch(package['sha256']))
        self.assertGreater(package['bytes'], 0)
        self.assertEqual(set(package['members']), {'index.html', 'floor-2000.png', 'floor-3000.png',
                                                  'floor-4000.png', 'README.txt'})
        self.assertEqual(package['archive_CRC_all_members_passed'], True)
        for floor in report['floors']:
            frame = floor['observation_png']
            self.assertEqual(package['members'][frame['file']], frame['sha256'])
        self.assertEqual(report['stage_a'], '7_PARTIAL_2_OPEN')
        self.assertEqual((report['stage_b'], report['wiki'], report['R79']),
                         ('GATED', 'GATED', 'PAUSED_NON_BLOCKING'))
        self.assertIsNone(report['overall_percent'])
        self.assertEqual(report['evidence_limits'], {
            'official_release_attributed': False,
            'original_runtime_executed': False,
            'native_draw_order_proven': False,
            'native_palette_proven': False,
            'native_dialogue_trigger_proven': False,
            'original_assets_in_public_git': False,
        })
        self.assertEqual(report['continuity']['preserved_current_blob'],
                         'c89e0e33537990aa2132b47c40fef49a985a935c')


if __name__ == '__main__':
    unittest.main()
