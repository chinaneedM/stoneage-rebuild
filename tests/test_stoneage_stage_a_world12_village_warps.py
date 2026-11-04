"""Cross-check the public joins without original DAT or CREATE assets."""

from collections import Counter
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1] / 'research' / 'recovered'
VILLAGES = {2000, 3000, 4000}


def load(glob):
    path, = ROOT.glob(glob)
    return json.loads(path.read_bytes())


class VillageWarps(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.char = load('*CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json')
        cls.map01 = load('*MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json')
        cls.recovery = load('*INDEPENDENT-RAR-MAP-PIXEL-RECOVERY-R1.json')
        cls.world10 = load('*CONTENT-10-THREE-VILLAGE-MAP-OBSERVATION-R1.json')
        cls.report = load('*CONTENT-12-THREE-VILLAGE-WARP-SOURCE-R1.json')

    def test_all_classic_create_centers_match_the_three_source_planes(self):
        report = self.report
        expected = {(row[0], row[1]): (row[4], row[5], row[7][:2])
                    for row in self.char['create_rows'] if row[5] in VILLAGES and row[11] == 'npcgen_warp'}
        self.assertEqual(len(expected), 73)
        self.assertEqual(expected, {(r['create_path'], r['create_ordinal']):
                                   (r['create_block_sha256'], r['floor'], r['xy']) for r in report['routes']})
        self.assertEqual(report['original_create_files_rechecked'], self.char['counts']['file_types']['create'])
        self.assertEqual(report['original_archive_sha256'], self.char['original_rar_sha256'])
        names = {r[0]: r[2] for r in self.char['source_files']}
        for r in report['routes']:
            self.assertEqual(r['original_create_sha256'], names[r['create_path']])
        for floor, n in ((2000, 27), (3000, 25), (4000, 21)):
            row = report['floors'][str(floor)]
            self.assertEqual((row['create_count'], row['marked_dat_count']), (n, n))
            self.assertEqual((row['only_create'], row['only_dat']), ([], []))
            self.assertEqual(sum(row['event_counts'].values()), 22500)
            source = Counter(r['source_DAT_u16'][2] for r in report['routes'] if r['floor'] == floor)
            self.assertEqual(source, {49155: n-2, 49158: 1, 49159: 1})
        actual = Counter((tuple(r['tail']), r['source_DAT_u16'][2]) for r in report['routes'])
        self.assertEqual(actual, {((), 49155): 67, (('M',), 49158): 3, (('A',), 49159): 3})

    def test_destination_members_and_cells(self):
        report = self.report
        targets = {r['destination'][0] for r in report['routes']}
        self.assertEqual(report['target_floors'], sorted(targets))
        self.assertEqual(len(targets), 35)
        maps = {row['floor']: row for row in report['dat_sources']}
        self.assertEqual(set(maps), targets | VILLAGES)
        self.assertEqual(len(maps), 38)
        known = {row[1].lower(): (row[2], row[3], row[4], row[6:8])
                 for row in self.map01['original_decoded_source_rows'] if row[0] == 0}
        for row in self.recovery['recovered_MAP01_failures']:
            if row['group'] == 0:
                known[row['name'].lower()] = row['bytes'], row['sha256'], row['crc32'], row['dimensions']
        for n, map_ in maps.items():
            name = map_['archive_member'].rsplit('/', 1)[1].lower()
            self.assertEqual(name, f'{n}.dat')
            self.assertEqual((map_['bytes'], map_['sha256'], map_['crc32'], map_['dimensions']), known[name])
        for prior in self.world10['floors']:
            original = prior['original_DAT']
            candidate = maps[prior['floor']]
            self.assertEqual(candidate['sha256'], original['sha256'])
            self.assertEqual(candidate['event_plane_sha256'], original['plane_sha256_little_endian'][2])
        for r in report['routes']:
            floor, x, y = r['destination']
            w, h = maps[floor]['dimensions']
            self.assertTrue(0 <= x < w and 0 <= y < h)
        self.assertEqual(Counter(r['destination_DAT_u16'][2] for r in report['routes']), {49155: 51, 49152: 22})

    def test_return_rows_keep_exact_and_other_targets_separate(self):
        rows = self.report['routes']
        scope = {tuple(r['destination']) for r in rows}
        by_arrival = {}
        for item in self.char['create_rows']:
            name, ordinal, _, _, sha, floor, _, corner, _, _, _, token, *_ = item
            if token == 'npcgen_warp' and corner and corner[:2] == corner[2:] and (floor, *corner[:2]) in scope:
                by_arrival.setdefault((floor, *corner[:2]), []).append((name, ordinal, sha))
        for route in rows:
            check = route['arrival_same_cell_CREATE']
            actual = [(r['create_path'], r['create_ordinal'], r['create_block_sha256']) for r in check['rows']]
            self.assertEqual(actual, by_arrival.get(tuple(route['destination']), []))
            if check['status'] == 'single_exact_reciprocal':
                self.assertEqual([r['destination'] for r in check['rows']], [[route['floor'], *route['xy']]])
            elif check['status'] == 'single_point_CREATE_with_different_target':
                self.assertEqual(len(check['rows']), 1)
                self.assertNotEqual(check['rows'][0]['destination'], [route['floor'], *route['xy']])
            else:
                self.assertEqual(check['status'], 'no_point_CREATE_at_arrival')
                self.assertEqual(check['rows'], [])
        totals = Counter(r['arrival_same_cell_CREATE']['status'] for r in rows)
        self.assertEqual(totals, {'single_exact_reciprocal': 49, 'no_point_CREATE_at_arrival': 22,
                                  'single_point_CREATE_with_different_target': 2})
        self.assertEqual(totals, self.report['arrival_same_cell_CREATE_counts'])

    def test_publication_and_stage_bounds(self):
        report = self.report
        self.assertEqual(len(report['bounds']), 4)
        self.assertTrue(all(flag is False for flag in report['bounds'].values()))
        self.assertEqual(report['continuity']['preserved_current_blob'], 'c89e0e33537990aa2132b47c40fef49a985a935c')
        self.assertEqual((report['stage_a'], report['stage_b'], report['wiki'], report['R79']),
                         ('7_PARTIAL_2_OPEN', 'GATED', 'GATED', 'PAUSED_NON_BLOCKING'))
        self.assertIsNone(report['overall_percent'])


if __name__ == '__main__':
    unittest.main()
